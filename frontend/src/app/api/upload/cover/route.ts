/* eslint-disable @typescript-eslint/no-unused-vars */
import { NextRequest, NextResponse } from 'next/server';

export async function POST(_request: NextRequest) {
  try {
    // TODO: Implement cover image upload logic
    return NextResponse.json(
      { message: 'Cover upload endpoint - Coming soon' },
      { status: 200 }
    );
  } catch (error) {
    console.error('Cover upload error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json(
    { message: 'Cover upload API endpoint' },
    { status: 200 }
  );
}
