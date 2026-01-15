import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  Chip,
  LinearProgress,
  Link,
  Divider,
} from '@mui/material';
import { marketAPI, NewsItem } from '../services/api';

interface NewsListProps {
  symbols?: string[];
  limit?: number;
}

const NewsList: React.FC<NewsListProps> = ({ symbols, limit = 10 }) => {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const data = await marketAPI.getNews(symbols, limit);
        setNews(data);
      } catch (error) {
        console.error('Failed to fetch news:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchNews();
    const interval = setInterval(fetchNews, 300000); // 5分ごとに更新

    return () => clearInterval(interval);
  }, [symbols, limit]);

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'critical':
        return 'error';
      case 'high':
        return 'warning';
      case 'medium':
        return 'info';
      default:
        return 'default';
    }
  };

  const getImpactLabel = (impact: string) => {
    switch (impact) {
      case 'critical':
        return '重大';
      case 'high':
        return '高';
      case 'medium':
        return '中';
      default:
        return '低';
    }
  };

  const getSentimentColor = (sentiment: number) => {
    if (sentiment > 0.2) return 'success';
    if (sentiment < -0.2) return 'error';
    return 'default';
  };

  const getSentimentLabel = (sentiment: number) => {
    if (sentiment > 0.2) return 'ポジティブ';
    if (sentiment < -0.2) return 'ネガティブ';
    return '中立';
  };

  if (loading) {
    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            最新ニュース
          </Typography>
          <LinearProgress />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          最新ニュース
        </Typography>

        <List>
          {news.map((item, index) => (
            <React.Fragment key={item.id}>
              {index > 0 && <Divider />}
              <ListItem alignItems="flex-start" sx={{ px: 0 }}>
                <ListItemText
                  primary={
                    <Box>
                      <Typography variant="subtitle1" component="span">
                        {item.url ? (
                          <Link href={item.url} target="_blank" rel="noopener noreferrer">
                            {item.title}
                          </Link>
                        ) : (
                          item.title
                        )}
                      </Typography>
                      <Box display="flex" gap={1} mt={1}>
                        <Chip
                          label={getImpactLabel(item.impact)}
                          size="small"
                          color={getImpactColor(item.impact) as any}
                        />
                        <Chip
                          label={getSentimentLabel(item.sentiment)}
                          size="small"
                          color={getSentimentColor(item.sentiment) as any}
                          variant="outlined"
                        />
                      </Box>
                    </Box>
                  }
                  secondary={
                    <Box mt={1}>
                      {item.description && (
                        <Typography variant="body2" color="text.secondary" paragraph>
                          {item.description}
                        </Typography>
                      )}
                      <Box display="flex" justifyContent="space-between" alignItems="center">
                        <Typography variant="caption" color="text.secondary">
                          {item.source} • {new Date(item.published_at).toLocaleString('ja-JP')}
                        </Typography>
                        {item.tags.length > 0 && (
                          <Box display="flex" gap={0.5}>
                            {item.tags.slice(0, 3).map((tag) => (
                              <Chip
                                key={tag}
                                label={tag}
                                size="small"
                                variant="outlined"
                                sx={{ fontSize: '0.7rem', height: 20 }}
                              />
                            ))}
                          </Box>
                        )}
                      </Box>
                    </Box>
                  }
                />
              </ListItem>
            </React.Fragment>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default NewsList;
