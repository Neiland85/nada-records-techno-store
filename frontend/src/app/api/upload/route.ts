import { put } from '@vercel/blob';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;
    const albumId = formData.get('albumId') as string;

    if (!file) {
      return NextResponse.json({ error: 'No file provided' }, { status: 400 });
    }

    if (!albumId) {
      return NextResponse.json(
        { error: 'No album ID provided' },
        { status: 400 }
      );
    }

    // Validar tipo de archivo
    const allowedTypes = [
      'audio/mpeg',
      'audio/wav',
      'audio/flac',
      'audio/aac',
      'audio/ogg',
    ];
    if (!allowedTypes.includes(file.type)) {
      return NextResponse.json(
        { error: 'Invalid file type. Only audio files are allowed.' },
        { status: 400 }
      );
    }

    // Validar tamaño de archivo (500MB máximo)
    const maxSize = 500 * 1024 * 1024;
    if (file.size > maxSize) {
      return NextResponse.json(
        { error: 'File too large. Maximum size is 500MB.' },
        { status: 400 }
      );
    }

    // Generar nombre único para el archivo
    const fileExtension = file.name.split('.').pop();
    const uniqueName = `${albumId}/${Date.now()}-${Math.random().toString(36).substring(2)}.${fileExtension}`;

    // Subir archivo a Vercel Blob
    const blob = await put(uniqueName, file, {
      access: 'public',
      contentType: file.type,
    });

    return NextResponse.json({
      uploadId: `upload_${Date.now()}`,
      fileUrl: blob.url,
      fileSize: file.size,
      filename: file.name,
      message: 'File uploaded successfully',
    });
  } catch (error) {
    console.error('Upload error:', error);
    return NextResponse.json(
      { error: 'Failed to upload file' },
      { status: 500 }
    );
  }
}
