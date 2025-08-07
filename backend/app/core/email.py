"""Email configuration and services using SendGrid."""

import os
from typing import Optional, Dict, Any, List
import json
import logging
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content, Email, To
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class EmailSettings(BaseSettings):
    """Email configuration settings."""
    
    # SendGrid Configuration
    sendgrid_api_key: str = ""
    sendgrid_from_email: str = "noreply@nadarecords.com"
    sendgrid_from_name: str = "Nada Records Techno Store"
    
    # SMTP Fallback Configuration
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    email_from_address: str = "noreply@nadarecords.com"
    
    # Email Templates
    email_templates_dir: str = "app/templates/email"
    
    class Config:
        env_file = ".env"
        env_prefix = ""
        extra = "ignore"


email_settings = EmailSettings()


class EmailService:
    """Email service using SendGrid API."""
    
    def __init__(self):
        """Initialize SendGrid client."""
        self.sendgrid_client = None
        if email_settings.sendgrid_api_key:
            try:
                self.sendgrid_client = SendGridAPIClient(api_key=email_settings.sendgrid_api_key)
                logger.info("SendGrid client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize SendGrid client: {e}")
        else:
            logger.warning("SendGrid API key not provided")
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        plain_content: Optional[str] = None,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
        attachments: Optional[list] = None
    ) -> bool:
        """
        Send email using SendGrid.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML content of the email
            plain_content: Plain text content (optional)
            from_email: Sender email (optional, uses default)
            from_name: Sender name (optional, uses default)
            attachments: List of attachments (optional)
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        if not self.sendgrid_client:
            logger.error("SendGrid client not initialized")
            return False
        
        try:
            # Set sender information
            sender_email = from_email or email_settings.sendgrid_from_email
            sender_name = from_name or email_settings.sendgrid_from_name
            
            # Create email
            from_email_obj = Email(email=sender_email, name=sender_name)
            to_email_obj = To(email=to_email)
            
            # Create mail object
            mail = Mail(
                from_email=from_email_obj,
                to_emails=to_email_obj,
                subject=subject,
                html_content=Content("text/html", html_content)
            )
            
            # Add plain text content if provided
            if plain_content:
                mail.content.append(Content("text/plain", plain_content))
            
            # Add attachments if provided
            if attachments:
                for attachment in attachments:
                    mail.add_attachment(attachment)
            
            # Send email
            response = self.sendgrid_client.send(mail)
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email: {response.status_code} - {response.body}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    async def send_welcome_email(self, to_email: str, user_name: str) -> bool:
        """
        Send welcome email to new user.
        
        Args:
            to_email: User's email address
            user_name: User's name
            
        Returns:
            bool: True if email sent successfully
        """
        subject = "¡Bienvenido a Nada Records Techno Store!"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                <h1 style="color: white; margin: 0;">🎵 Nada Records</h1>
                <p style="color: white; margin: 10px 0 0 0;">Techno Store</p>
            </div>
            
            <div style="padding: 30px; background-color: #f9f9f9;">
                <h2 style="color: #333; margin-bottom: 20px;">¡Hola {user_name}!</h2>
                
                <p style="color: #666; line-height: 1.6;">
                    ¡Bienvenido a <strong>Nada Records Techno Store</strong>! Estamos emocionados de tenerte 
                    como parte de nuestra comunidad de amantes del techno.
                </p>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #333; margin-top: 0;">🎧 ¿Qué puedes hacer ahora?</h3>
                    <ul style="color: #666; line-height: 1.6;">
                        <li>Explorar nuestra colección de tracks techno exclusivos</li>
                        <li>Descargar samples y loops de alta calidad</li>
                        <li>Acceder a contenido premium para productores</li>
                        <li>Conectar con otros artistas de la comunidad</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{os.getenv('FRONTEND_URL', 'http://localhost:3000')}" 
                       style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                              color: white; padding: 15px 30px; text-decoration: none; 
                              border-radius: 25px; display: inline-block; font-weight: bold;">
                        🚀 Comenzar Ahora
                    </a>
                </div>
                
                <p style="color: #666; line-height: 1.6;">
                    Si tienes alguna pregunta, no dudes en contactarnos. ¡Estamos aquí para ayudarte!
                </p>
                
                <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                
                <p style="color: #999; font-size: 14px; text-align: center;">
                    Nada Records Techno Store<br>
                    El futuro del techno está aquí 🔊
                </p>
            </div>
        </body>
        </html>
        """
        
        plain_content = f"""
        ¡Hola {user_name}!
        
        ¡Bienvenido a Nada Records Techno Store! Estamos emocionados de tenerte como parte de nuestra comunidad.
        
        ¿Qué puedes hacer ahora?
        - Explorar nuestra colección de tracks techno exclusivos
        - Descargar samples y loops de alta calidad
        - Acceder a contenido premium para productores
        - Conectar con otros artistas de la comunidad
        
        Visita nuestra tienda: {os.getenv('FRONTEND_URL', 'http://localhost:3000')}
        
        ¡El futuro del techno está aquí!
        
        Nada Records Techno Store
        """
        
        return await self.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            plain_content=plain_content
        )
    
    async def send_purchase_confirmation(
        self, 
        to_email: str, 
        user_name: str, 
        order_details: Dict[str, Any]
    ) -> bool:
        """
        Send purchase confirmation email.
        
        Args:
            to_email: User's email address
            user_name: User's name
            order_details: Dictionary with order information
            
        Returns:
            bool: True if email sent successfully
        """
        order_id = order_details.get('order_id', 'N/A')
        total_amount = order_details.get('total_amount', 0)
        items = order_details.get('items', [])
        
        subject = f"✅ Confirmación de Compra - Orden #{order_id}"
        
        # Generate items HTML
        items_html = ""
        for item in items:
            items_html += f"""
            <tr style="border-bottom: 1px solid #eee;">
                <td style="padding: 10px; color: #333;">{item.get('name', 'N/A')}</td>
                <td style="padding: 10px; color: #333; text-align: center;">{item.get('type', 'Track')}</td>
                <td style="padding: 10px; color: #333; text-align: right;">${item.get('price', 0):.2f}</td>
            </tr>
            """
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                <h1 style="color: white; margin: 0;">🎵 Nada Records</h1>
                <p style="color: white; margin: 10px 0 0 0;">Confirmación de Compra</p>
            </div>
            
            <div style="padding: 30px; background-color: #f9f9f9;">
                <h2 style="color: #333;">¡Gracias por tu compra, {user_name}!</h2>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #333; margin-top: 0;">📋 Detalles de la Orden</h3>
                    <p><strong>Número de Orden:</strong> #{order_id}</p>
                    <p><strong>Total:</strong> ${total_amount:.2f}</p>
                    
                    <table style="width: 100%; margin-top: 20px; border-collapse: collapse;">
                        <thead>
                            <tr style="background-color: #f5f5f5;">
                                <th style="padding: 10px; text-align: left; color: #333;">Producto</th>
                                <th style="padding: 10px; text-align: center; color: #333;">Tipo</th>
                                <th style="padding: 10px; text-align: right; color: #333;">Precio</th>
                            </tr>
                        </thead>
                        <tbody>
                            {items_html}
                        </tbody>
                    </table>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/downloads" 
                       style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                              color: white; padding: 15px 30px; text-decoration: none; 
                              border-radius: 25px; display: inline-block; font-weight: bold;">
                        📥 Descargar Archivos
                    </a>
                </div>
                
                <p style="color: #666; line-height: 1.6;">
                    Tus archivos están listos para descargar. Los enlaces de descarga estarán disponibles 
                    en tu cuenta por 30 días.
                </p>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content
        )
    
    async def send_password_reset(self, to_email: str, reset_token: str) -> bool:
        """
        Send password reset email.
        
        Args:
            to_email: User's email address
            reset_token: Password reset token
            
        Returns:
            bool: True if email sent successfully
        """
        subject = "🔐 Restablecer Contraseña - Nada Records"
        
        reset_url = f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/reset-password?token={reset_token}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                <h1 style="color: white; margin: 0;">🎵 Nada Records</h1>
                <p style="color: white; margin: 10px 0 0 0;">Restablecer Contraseña</p>
            </div>
            
            <div style="padding: 30px; background-color: #f9f9f9;">
                <h2 style="color: #333;">Solicitud de Restablecimiento</h2>
                
                <p style="color: #666; line-height: 1.6;">
                    Recibimos una solicitud para restablecer la contraseña de tu cuenta.
                </p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_url}" 
                       style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                              color: white; padding: 15px 30px; text-decoration: none; 
                              border-radius: 25px; display: inline-block; font-weight: bold;">
                        🔐 Restablecer Contraseña
                    </a>
                </div>
                
                <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <p style="color: #856404; margin: 0; font-size: 14px;">
                        ⚠️ Este enlace expirará en 1 hora por seguridad.
                    </p>
                </div>
                
                <p style="color: #666; line-height: 1.6; font-size: 14px;">
                    Si no solicitaste este restablecimiento, puedes ignorar este email de forma segura.
                </p>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content
        )


# Global email service instance
email_service = EmailService()


async def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    plain_content: Optional[str] = None
) -> bool:
    """Convenience function to send email."""
    return await email_service.send_email(
        to_email=to_email,
        subject=subject,
        html_content=html_content,
        plain_content=plain_content
    )


async def send_welcome_email(to_email: str, user_name: str) -> bool:
    """Convenience function to send welcome email."""
    return await email_service.send_welcome_email(to_email, user_name)


async def send_purchase_confirmation(
    to_email: str, 
    user_name: str, 
    order_details: Dict[str, Any]
) -> bool:
    """Convenience function to send purchase confirmation."""
    return await email_service.send_purchase_confirmation(to_email, user_name, order_details)


async def send_password_reset(to_email: str, reset_token: str) -> bool:
    """Convenience function to send password reset email."""
    return await email_service.send_password_reset(to_email, reset_token)
