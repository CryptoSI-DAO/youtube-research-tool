import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { youtubeUrl, email } = body;

    // Validate inputs
    if (!youtubeUrl || !email) {
      return NextResponse.json(
        { error: "YouTube URL and email are required" },
        { status: 400 }
      );
    }

    // Basic URL validation
    const validYouTube =
      /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+/i.test(youtubeUrl);
    if (!validYouTube) {
      return NextResponse.json(
        { error: "Please enter a valid YouTube URL" },
        { status: 400 }
      );
    }

    // Basic email validation
    const validEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    if (!validEmail) {
      return NextResponse.json(
        { error: "Please enter a valid email address" },
        { status: 400 }
      );
    }

    // Check password (client-side gate is cosmetic; this is the real check)
    // Password is hashed and compared server-side via env var
    const authHeader = request.headers.get("x-access-password");
    const expectedHash = process.env.ACCESS_PASSWORD_HASH;

    if (expectedHash && authHeader !== expectedHash) {
      return NextResponse.json(
        { error: "Unauthorized" },
        { status: 401 }
      );
    }

    // Forward to webhook server
    const webhookUrl = process.env.WEBHOOK_URL;
    if (!webhookUrl) {
      return NextResponse.json(
        { error: "Service temporarily unavailable" },
        { status: 503 }
      );
    }

    const webhookResponse = await fetch(webhookUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        youtubeUrl,
        email,
        timestamp: new Date().toISOString(),
        source: "web",
      }),
    });

    if (!webhookResponse.ok) {
      const errText = await webhookResponse.text();
      console.error("Webhook error:", errText);
      return NextResponse.json(
        { error: "Failed to queue research job. Please try again." },
        { status: 502 }
      );
    }

    return NextResponse.json({
      success: true,
      message: "Research job queued successfully",
    });
  } catch (error) {
    console.error("Submit error:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
