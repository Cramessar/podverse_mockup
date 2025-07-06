//item ednpoint
//Item Endpoints (item_bp):

//GET /items — Get all items
//GET /items/<int:item_id> — Get a specific item by ID (via query param)
//GET /items/channel/<int:channel_id> — Get items by channel ID (via query param)
//POST /items — Create a new item
//PUT /items/<int:item_id> — Update an item

// frontend/app/api/categories/route.ts

import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({ message: "Items endpoint works!" });
}