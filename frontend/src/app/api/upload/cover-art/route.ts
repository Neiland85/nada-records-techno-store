import { NextRequest, NextResponse } from 'next/server';
import { put, del } from '@vercel/blob';
import { z } from 'zod';

// Validation schema for cover art upload
const coverArtSchema = z.object({
  albumId: z.string().uuid(),
});

// Maximum file size for images (10MB)
const MAX_IMAGE_SIZE = 10 * 1024 * 1024;

// Supported image formats
const SUPPORTED_FORMATS = ['image/jpeg', 'image/png', 'image/webp'];

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;
    const albumId = formData.get('albumId') as string;

    // Validate input
    const validationResult = coverArtSchema.safeParse({ albumId });

    if (!validationResult.success) {
      return NextResponse.json(
        { error: 'Invalid input', details: validationResult.error.issues },
        { status: 400 }
      );
    }

    // Validate file
    if (!file) {
      return NextResponse.json(
        { error: 'No file provided' },
        { status: 400 }
      );
    }

    // Check file type
    if (!SUPPORTED_FORMATS.includes(file.type)) {
      return NextResponse.json(
        { error: `Unsupported image format. Supported: ${SUPPORTED_FORMATS.join(', ')}` },
        { status: 400 }
      );
    }

    // Check file size
    if (file.size > MAX_IMAGE_SIZE) {
      return NextResponse.json(
        { error: `Image size exceeds maximum limit of ${MAX_IMAGE_SIZE / (1024 * 1024)}MB` },
        { status: 413 }
      );
    }

    // Generate unique filename
    const fileExtension = file.name.split('.').pop();
    const timestamp = Date.now();
    const randomId = Math.random().toString(36).substring(2, 15);
    const filename = `covers/${albumId}/${timestamp}_${randomId}.${fileExtension}`;

    // Upload to Vercel Blob
    const blob = await put(filename, file, {
      access: 'public',
      contentType: file.type,
    });

    // Here you would typically:
    // 1. Save cover art URL to your database
    // 2. Generate different sizes (thumbnail, medium, large)
    // 3. Update album record

    return NextResponse.json({
      success: true,
      uploadId: randomId,
      fileUrl: blob.url,
      fileSize: file.size,
      filename: file.name,
      contentType: file.type,
      uploadedAt: new Date().toISOString(),
    });

  } catch (error) {
    console.error('Cover art upload error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// Handle cover art deletion
export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const fileUrl = searchParams.get('fileUrl');

    if (!fileUrl) {
      return NextResponse.json(
        { error: 'File URL required' },
        { status: 400 }
      );
    }

    // Delete from Vercel Blob
    await del(fileUrl);

    return NextResponse.json({
      success: true,
      message: 'Cover art deleted successfully'
    });

  } catch (error) {
    console.error('Delete error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
