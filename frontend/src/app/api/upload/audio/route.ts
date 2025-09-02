import { del, put } from '@vercel/blob';
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

// Validation schema for audio upload
const audioUploadSchema = z.object({
  title: z.string().min(1).max(200),
  albumId: z.string().uuid(),
  trackNumber: z.number().min(1),
  genre: z.string().optional(),
});

// Maximum file size (500MB)
const MAX_FILE_SIZE = 500 * 1024 * 1024;

export async function POST(request: NextRequest) {
  try {
    // Check authentication (you'll need to implement this)
    // const session = await getServerSession();
    // if (!session) {
    //   return NextResponse.json(
    //     { error: 'Unauthorized' },
    //     { status: 401 }
    //   );
    // }

    const formData = await request.formData();
    const file = formData.get('file') as File;
    const title = formData.get('title') as string;
    const albumId = formData.get('albumId') as string;
    const trackNumber = parseInt(formData.get('trackNumber') as string);
    const genre = formData.get('genre') as string;

    // Validate input
    const validationResult = audioUploadSchema.safeParse({
      title,
      albumId,
      trackNumber,
      genre,
    });

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
    if (!file.type.startsWith('audio/')) {
      return NextResponse.json(
        { error: 'File must be an audio file' },
        { status: 400 }
      );
    }

    // Check file size
    if (file.size > MAX_FILE_SIZE) {
      return NextResponse.json(
        { error: `File size exceeds maximum limit of ${MAX_FILE_SIZE / (1024 * 1024)}MB` },
        { status: 413 }
      );
    }

    // Generate unique filename
    const fileExtension = file.name.split('.').pop();
    const timestamp = Date.now();
    const uniqueFilename = `audio/${albumId}/${trackNumber}_${title.replace(/[^a-zA-Z0-9]/g, '_')}_${timestamp}.${fileExtension}`;

    // Upload to Vercel Blob
    const blob = await put(uniqueFilename, file, {
      access: 'public',
      contentType: file.type,
    });

    // Here you would typically:
    // 1. Save file metadata to your database
    // 2. Extract audio metadata (duration, bitrate, etc.)
    // 3. Generate preview
    // 4. Create track record

    // For now, return the upload result
    return NextResponse.json({
      success: true,
      uploadId: `upload_${timestamp}`,
      fileUrl: blob.url,
      fileSize: file.size,
      filename: uniqueFilename,
      message: 'File uploaded successfully',
      // TODO: Add more metadata from audio processing
    });

  } catch (error) {
    console.error('Audio upload error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// Optional: Handle file deletion
export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const fileUrl = searchParams.get('fileUrl');

    if (!fileUrl) {
      return NextResponse.json(
        { error: 'File URL is required' },
        { status: 400 }
      );
    }

    // Delete from Vercel Blob
    await del(fileUrl);

    return NextResponse.json({
      success: true,
      message: 'File deleted successfully'
    });

  } catch (error) {
    console.error('File deletion error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
