export type YappyClipzStatus =
  | 'queued'
  | 'analyzing'
  | 'editing'
  | 'rendering'
  | 'qa'
  | 'ready'
  | 'approved'
  | 'failed'
  | 'rejected'
  | 'cancelled';

export type OutputKind = 'mp4' | 'capcut';

export interface YappyClipzClientOptions {
  baseUrl: string;
  token: string;
  fetchImpl?: typeof fetch;
}

export interface CreateProjectInput {
  tenant_id: string;
  name: string;
  brand_profile_id?: string;
  metadata?: Record<string, unknown>;
}

export interface AddAssetInput {
  tenant_id: string;
  kind: 'video' | 'audio' | 'image' | 'subtitle' | 'logo' | 'other';
  source_url: string;
  filename?: string;
  checksum_sha256?: string;
  metadata?: Record<string, unknown>;
}

export interface CreateSocialReelJobInput {
  tenant_id: string;
  recipe: 'social_reel_v1';
  source_asset_ids: string[];
  instructions?: {
    duration_seconds?: number;
    width?: 1080;
    height?: 1920;
    captions?: boolean;
    hook?: boolean;
    cta?: boolean;
    platform?: 'instagram' | 'tiktok' | 'youtube_shorts' | 'facebook_reels';
    notes?: string;
  };
  outputs: OutputKind[];
  idempotency_key?: string;
}

export interface Project {
  id: string;
  tenant_id: string;
  name: string;
  status: 'draft' | 'active' | 'ready' | 'approved' | 'rejected';
  created_at: string;
  updated_at?: string;
}

export interface Asset extends AddAssetInput {
  id: string;
}

export interface Job {
  id: string;
  project_id: string;
  tenant_id: string;
  recipe: string;
  status: YappyClipzStatus;
  progress?: number;
  error?: { code?: string; message?: string; retryable?: boolean } | null;
  created_at: string;
  updated_at?: string;
}

export interface Output {
  id: string;
  kind: 'mp4' | 'capcut' | 'thumbnail' | 'caption_text' | 'metadata';
  status: 'pending' | 'ready' | 'failed';
  url?: string;
  checksum_sha256?: string;
  width?: number;
  height?: number;
  duration_seconds?: number;
  verified?: boolean;
}

export class YappyClipzClient {
  private readonly baseUrl: string;
  private readonly token: string;
  private readonly fetchImpl: typeof fetch;

  constructor(options: YappyClipzClientOptions) {
    this.baseUrl = options.baseUrl.replace(/\/$/, '');
    this.token = options.token;
    this.fetchImpl = options.fetchImpl ?? fetch;
  }

  private async request<T>(path: string, init: RequestInit = {}): Promise<T> {
    const response = await this.fetchImpl(`${this.baseUrl}${path}`, {
      ...init,
      headers: {
        'content-type': 'application/json',
        authorization: `Bearer ${this.token}`,
        ...(init.headers ?? {}),
      },
    });

    if (!response.ok) {
      const body = await response.text();
      throw new Error(`YAPPY-CLIPZ ${response.status}: ${body.slice(0, 500)}`);
    }

    return (await response.json()) as T;
  }

  createProject(input: CreateProjectInput): Promise<Project> {
    return this.request('/api/v1/projects', {
      method: 'POST',
      body: JSON.stringify(input),
    });
  }

  addAsset(projectId: string, input: AddAssetInput): Promise<Asset> {
    return this.request(`/api/v1/projects/${encodeURIComponent(projectId)}/assets`, {
      method: 'POST',
      body: JSON.stringify(input),
    });
  }

  createSocialReelJob(projectId: string, input: CreateSocialReelJobInput): Promise<Job> {
    return this.request(`/api/v1/projects/${encodeURIComponent(projectId)}/jobs`, {
      method: 'POST',
      body: JSON.stringify(input),
    });
  }

  getJob(jobId: string, signal?: AbortSignal): Promise<Job> {
    return this.request(`/api/v1/jobs/${encodeURIComponent(jobId)}`, { signal });
  }

  getProject(projectId: string): Promise<Project> {
    return this.request(`/api/v1/projects/${encodeURIComponent(projectId)}`);
  }

  getOutputs(projectId: string): Promise<{ project_id: string; outputs: Output[] }> {
    return this.request(`/api/v1/projects/${encodeURIComponent(projectId)}/outputs`);
  }

  approve(projectId: string, approvedBy: string, outputId?: string): Promise<Project> {
    return this.request(`/api/v1/projects/${encodeURIComponent(projectId)}/approve`, {
      method: 'POST',
      body: JSON.stringify({ approved_by: approvedBy, output_id: outputId }),
    });
  }

  async waitForReady(jobId: string, options: { timeoutMs?: number; pollMs?: number } = {}): Promise<Job> {
    const timeoutMs = options.timeoutMs ?? 10 * 60_000;
    const pollMs = options.pollMs ?? 2_000;
    const deadline = Date.now() + timeoutMs;

    while (Date.now() < deadline) {
      const remainingMs = deadline - Date.now();
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), remainingMs);

      try {
        const job = await this.getJob(jobId, controller.signal);
        if (job.status === 'ready' || job.status === 'approved') return job;
        if (job.status === 'failed' || job.status === 'rejected' || job.status === 'cancelled') {
          throw new Error(`YAPPY-CLIPZ job ${job.id} ended in ${job.status}: ${job.error?.message ?? 'no error detail'}`);
        }
      } catch (error) {
        if (controller.signal.aborted && Date.now() >= deadline) {
          throw new Error(`YAPPY-CLIPZ job ${jobId} timed out after ${timeoutMs}ms`);
        }
        throw error;
      } finally {
        clearTimeout(timer);
      }

      const sleepMs = Math.min(pollMs, Math.max(0, deadline - Date.now()));
      if (sleepMs > 0) {
        await new Promise((resolve) => setTimeout(resolve, sleepMs));
      }
    }

    throw new Error(`YAPPY-CLIPZ job ${jobId} timed out after ${timeoutMs}ms`);
  }
}
