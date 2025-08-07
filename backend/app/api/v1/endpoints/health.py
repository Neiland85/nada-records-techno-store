"""
Health check endpoint for monitoring system status.

This endpoint provides comprehensive health checks for all system components
including database, cache, storage, and external services.
"""

import asyncio
import logging
import time
from pathlib import Path
from typing import Any, Dict

import redis
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.database import get_async_session
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


class HealthChecker:
    """Handles health checks for various system components."""

    @staticmethod
    async def check_database(session: AsyncSession) -> Dict[str, Any]:
        """Check database connectivity and basic functionality."""
        try:
            start_time = time.time()

            # Test basic connection
            result = await session.execute(text("SELECT 1"))
            result.fetchone()

            # Test table existence
            table_check = await session.execute(
                text(
                    """
                SELECT COUNT(*) FROM information_schema.tables
                WHERE table_schema = 'public'
            """
                )
            )
            table_count = table_check.scalar()

            response_time = round((time.time() - start_time) * 1000, 2)

            return {
                "status": "healthy",
                "response_time_ms": response_time,
                "tables_count": table_count,
                "connection": "active",
            }

        except SQLAlchemyError as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "connection": "failed"}
        except Exception as e:
            logger.error(f"Unexpected database error: {e}")
            return {
                "status": "unhealthy",
                "error": f"Unexpected error: {str(e)}",
                "connection": "unknown",
            }

    @staticmethod
    async def check_redis() -> Dict[str, Any]:
        """Check Redis connectivity and performance."""
        try:
            start_time = time.time()

            # Create Redis connection
            redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD,
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5,
            )

            # Test basic operations
            test_key = "health_check_test"
            redis_client.set(test_key, "test_value", ex=10)
            retrieved_value = redis_client.get(test_key)
            redis_client.delete(test_key)

            # Get Redis info
            redis_info = redis_client.info()
            response_time = round((time.time() - start_time) * 1000, 2)

            redis_client.close()

            return {
                "status": "healthy",
                "response_time_ms": response_time,
                "version": redis_info.get("redis_version"),
                "connected_clients": redis_info.get("connected_clients"),
                "memory_usage": redis_info.get("used_memory_human"),
                "operation_test": (
                    "passed" if retrieved_value == "test_value" else "failed"
                ),
            }

        except redis.RedisError as e:
            logger.error(f"Redis health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "connection": "failed"}
        except Exception as e:
            logger.error(f"Unexpected Redis error: {e}")
            return {
                "status": "unhealthy",
                "error": f"Unexpected error: {str(e)}",
                "connection": "unknown",
            }

    @staticmethod
    async def check_storage() -> Dict[str, Any]:
        """Check storage accessibility and required directories."""
        try:
            # Check if required directories exist or can be created
            required_dirs = [
                Path(settings.UPLOAD_DIR),
                Path(settings.UPLOAD_DIR) / "tracks",
                Path(settings.UPLOAD_DIR) / "covers",
                Path(settings.UPLOAD_DIR) / "previews",
                Path(settings.UPLOAD_DIR) / "waveforms",
            ]

            directories_status = {}

            for directory in required_dirs:
                try:
                    directory.mkdir(parents=True, exist_ok=True)
                    # Test write permissions
                    test_file = directory / ".health_check"
                    test_file.write_text("test")
                    test_file.unlink()

                    directories_status[str(directory)] = {
                        "exists": True,
                        "writable": True,
                        "status": "healthy",
                    }
                except Exception as e:
                    directories_status[str(directory)] = {
                        "exists": directory.exists(),
                        "writable": False,
                        "status": "unhealthy",
                        "error": str(e),
                    }

            # Check overall storage health
            all_healthy = all(
                dir_status["status"] == "healthy"
                for dir_status in directories_status.values()
            )

            return {
                "status": "healthy" if all_healthy else "unhealthy",
                "directories": directories_status,
                "upload_dir": str(settings.UPLOAD_DIR),
            }

        except Exception as e:
            logger.error(f"Storage health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": f"Storage check failed: {
                    str(e)}"}

    @staticmethod
    async def check_audio_tools() -> Dict[str, Any]:
        """Check if audio processing tools are available."""
        try:
            tools_status = {}

            # Check for required audio processing tools
            required_tools = ["ffmpeg", "ffprobe"]

            for tool in required_tools:
                try:
                    process = await asyncio.create_subprocess_exec(
                        tool,
                        "-version",
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                    )
                    stdout, stderr = await process.communicate()

                    if process.returncode == 0:
                        # Extract version information
                        version_info = (stdout.decode().split(
                            "\n")[0] if stdout else "Unknown")
                        tools_status[tool] = {
                            "available": True,
                            "version": version_info,
                            "status": "healthy",
                        }
                    else:
                        tools_status[tool] = {
                            "available": False,
                            "status": "unhealthy",
                            "error": stderr.decode() if stderr else "Tool not found",
                        }

                except Exception as e:
                    tools_status[tool] = {
                        "available": False,
                        "status": "unhealthy",
                        "error": str(e),
                    }

            all_tools_available = all(
                tool_status["available"] for tool_status in tools_status.values())

            return {
                "status": "healthy" if all_tools_available else "degraded",
                "tools": tools_status,
            }

        except Exception as e:
            logger.error(f"Audio tools health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": f"Audio tools check failed: {str(e)}",
            }


@router.get(
    "/health",
    summary="System Health Check",
    description="Comprehensive health check for all system components",
)
async def health_check(
    session: AsyncSession = Depends(get_async_session),
) -> Dict[str, Any]:
    """
    Perform comprehensive health check of all system components.

    Checks:
    - Database connectivity and performance
    - Redis cache connectivity
    - Storage accessibility and permissions
    - Audio processing tools availability
    - Overall system status

    Returns detailed status information for monitoring and debugging.
    """
    start_time = time.time()

    try:
        # Run all health checks concurrently
        health_tasks = await asyncio.gather(
            HealthChecker.check_database(session),
            HealthChecker.check_redis(),
            HealthChecker.check_storage(),
            HealthChecker.check_audio_tools(),
            return_exceptions=True,
        )

        database_health, redis_health, storage_health, audio_tools_health = health_tasks

        # Handle any exceptions from concurrent execution
        checks = {
            "database": (
                database_health
                if not isinstance(database_health, Exception)
                else {"status": "unhealthy", "error": str(database_health)}
            ),
            "redis": (
                redis_health
                if not isinstance(redis_health, Exception)
                else {"status": "unhealthy", "error": str(redis_health)}
            ),
            "storage": (
                storage_health
                if not isinstance(storage_health, Exception)
                else {"status": "unhealthy", "error": str(storage_health)}
            ),
            "audio_tools": (
                audio_tools_health
                if not isinstance(audio_tools_health, Exception)
                else {"status": "unhealthy", "error": str(audio_tools_health)}
            ),
        }

        # Determine overall system status
        critical_components = ["database", "redis", "storage"]
        critical_healthy = all(
            checks[component]["status"] == "healthy"
            for component in critical_components
        )

        if critical_healthy:
            if checks["audio_tools"]["status"] == "healthy":
                overall_status = "healthy"
            else:
                overall_status = "degraded"  # Audio tools are not critical
        else:
            overall_status = "unhealthy"

        total_time = round((time.time() - start_time) * 1000, 2)

        response = {
            "status": overall_status,
            "timestamp": int(time.time()),
            "response_time_ms": total_time,
            "version": "1.0.0",
            "environment": settings.ENVIRONMENT,
            "checks": checks,
        }

        # Log health check results
        if overall_status != "healthy":
            logger.warning(
                f"Health check completed with status: {overall_status}")
        else:
            logger.info(
                f"Health check completed successfully in {total_time}ms")

        return response

    except Exception as e:
        logger.error(f"Health check failed with unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "error": "Health check failed",
                "details": str(e),
            },
        )


@router.get(
    "/health/quick",
    summary="Quick Health Check",
    description="Basic health check for load balancer",
)
async def quick_health_check() -> Dict[str, str]:
    """
    Quick health check endpoint for load balancers and monitoring systems.

    Returns a simple status without detailed component checks.
    """
    return {"status": "healthy", "message": "Service is running"}
