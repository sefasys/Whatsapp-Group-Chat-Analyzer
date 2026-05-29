// ─── Base TypeScript Interfaces ───────────────────────────────────
export interface Message {
  id: string;
  timestamp: string;
  senderId: string;
  content: string;
  type: 'text' | 'media' | 'link' | 'system' | 'reaction' | 'deleted';
  emojis: string[];
  links: string[];
  isReply: boolean;
  replyToId?: string;
  wordCount: number;
}

export interface ActivityStats {
  totalMessages: number;
  totalWords: number;
  mediaCount: number;
  linkCount: number;
  emojiCount: number;
  avgMessageLength: number;
  messagesPerDay: number;
  mostActiveHour: number;
  mostActiveDay: string;
  firstMessageDate: string;
  lastMessageDate: string;
  silencePeriods: SilencePeriod[];
}

export interface SilencePeriod {
  start: string;
  end: string;
  durationDays: number;
  groupActivityLevel: 'low' | 'medium' | 'high';
}

export interface OceanScores {
  openness: number;
  conscientiousness: number;
  extraversion: number;
  agreeableness: number;
  neuroticism: number;
  confidence: number;
}

export interface SocialRole {
  primaryRole: string;
  secondaryRoles: string[];
  influenceScore: number;
  centralityScore: number;
}

export interface IdeologicalProfile {
  individualismCollectivism: number;
  authorityOrientation: string;
  keyValues: string[];
  recurringThemes: string[];
  politicalSignals: string[];
}

export interface CommunicationStyle {
  humorType: string;
  emojiPersonality: string;
  aggressionLevel: number;
  formalityLevel: number;
  topEmojis: string[];
  topWords: string[];
  avgResponseTimeMin?: number;
}

export interface UserProfile {
  userId: string;
  displayName: string;
  activity: ActivityStats;
  ocean: OceanScores;
  socialRole: SocialRole;
  ideology: IdeologicalProfile;
  communication: CommunicationStyle;
  llmNarrative: string;
  silentObserver: boolean;
}

export interface GroupReport {
  sessionId: string;
  dateRange: { start: string; end: string };
  totalMessages: number;
  activeUsers: UserProfile[];
  silentUsers: UserProfile[];
  groupDynamicsSummary: string;
  networkGraph: NetworkGraph;
  groupStats: GroupStats;
}

export interface NetworkGraph {
  nodes: NetworkNode[];
  edges: NetworkEdge[];
}

export interface NetworkNode {
  id: string;
  label: string;
  influenceScore: number;
  primaryRole: string;
}

export interface NetworkEdge {
  source: string;
  target: string;
  weight: number;
}

export interface GroupStats {
  totalMessages?: number;
  dailyActivity: { date: string; count: number }[];
  hourlyHeatmap: number[][];
  topicDistribution: { topic: string; percentage: number }[];
  sentimentOverTime: { date: string; score: number }[];
}

export type AnalysisStatus = 'idle' | 'uploading' | 'parsing' | 'analyzing' | 'completed' | 'error';
