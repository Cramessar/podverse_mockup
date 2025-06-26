import { GET, PUT, DELETE } from './route';
import { NextRequest } from 'next/server';

jest.mock('axios', () => ({
  get: jest.fn().mockResolvedValue({ data: { id: 1, title: 'Feed 1' }, status: 200 }),
  put: jest.fn().mockResolvedValue({ data: { id: 1, title: 'Updated Feed' }, status: 200 }),
  delete: jest.fn().mockResolvedValue({ data: { success: true }, status: 200 }),
}));

jest.mock('@/lib/auth0', () => ({
  auth0: { getSession: jest.fn().mockResolvedValue({ accessToken: 'fake-token' }) }
}));

const mockParams = { params: { feed_id: '1' } };

describe('/api/feeds/[feed_id] API Route', () => {
  it('GET returns a feed by ID', async () => {
    const req = {} as NextRequest;
    const res = await GET(req, mockParams);
    const json = await res.json();
    expect(res.status).toBe(200);
    expect(json).toHaveProperty('id', 1);
    expect(json).toHaveProperty('title', 'Feed 1');
  });

  it('PUT updates a feed by ID', async () => {
    const req = {
      json: async () => ({ title: 'Updated Feed' })
    } as unknown as NextRequest;
    const res = await PUT(req, mockParams);
    const json = await res.json();
    expect(res.status).toBe(200);
    expect(json).toHaveProperty('title', 'Updated Feed');
  });

  it('DELETE deletes a feed by ID', async () => {
    const req = {} as NextRequest;
    const res = await DELETE(req, mockParams);
    const json = await res.json();
    expect(res.status).toBe(200);
    expect(json).toHaveProperty('success', true);
  });
});