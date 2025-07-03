import { GET, POST } from './route';
import { NextRequest } from 'next/server';

jest.mock('axios', () => ({
  get: jest.fn().mockResolvedValue({ data: [{ id: 1, title: 'Feed 1' }], status: 200 }),
  post: jest.fn().mockResolvedValue({ data: { id: 2, title: 'New Feed' }, status: 201 }),
}));

jest.mock('@/lib/auth0', () => ({
  auth0: { getSession: jest.fn().mockResolvedValue({ accessToken: 'fake-token' }) }
}));

describe('/api/feeds API Route', () => {
it('GET returns all feeds', async () => {
  const req = {
    nextUrl: {
      searchParams: {
        toString: () => "" // or return a query string if you want to test with params
      }
    }
  } as unknown as NextRequest;
  const res = await GET(req);
  const json = await res.json();
  expect(res.status).toBe(200);
  expect(Array.isArray(json)).toBe(true);
  expect(json[0]).toHaveProperty('title', 'Feed 1');
});

  it('POST creates a new feed', async () => {
    const req = {
      json: async () => ({ title: 'New Feed' })
    } as unknown as NextRequest;
    const res = await POST(req);
    const json = await res.json();
    expect(res.status).toBe(201);
    expect(json).toHaveProperty('title', 'New Feed');
  });
});