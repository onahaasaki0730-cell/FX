import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  LinearProgress,
  Paper,
} from '@mui/material';
import { marketAPI, TrendAnalysis as TrendAnalysisType } from '../services/api';

interface TrendAnalysisProps {
  symbol: string;
  timeframes: string[];
}

const TrendAnalysis: React.FC<TrendAnalysisProps> = ({ symbol, timeframes }) => {
  const [analyses, setAnalyses] = useState<Record<string, TrendAnalysisType>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalyses = async () => {
      try {
        const results: Record<string, TrendAnalysisType> = {};
        
        for (const tf of timeframes) {
          const data = await marketAPI.getTrend(symbol, tf);
          results[tf] = data;
        }
        
        setAnalyses(results);
      } catch (error) {
        console.error('Failed to fetch trend analyses:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalyses();
    const interval = setInterval(fetchAnalyses, 300000); // 5分ごとに更新

    return () => clearInterval(interval);
  }, [symbol, timeframes]);

  const getTrendColor = (direction: string) => {
    switch (direction) {
      case 'bullish':
        return 'success';
      case 'bearish':
        return 'error';
      case 'sideways':
        return 'warning';
      default:
        return 'default';
    }
  };

  const getTrendLabel = (direction: string) => {
    switch (direction) {
      case 'bullish':
        return '上昇トレンド';
      case 'bearish':
        return '下降トレンド';
      case 'sideways':
        return 'レンジ';
      default:
        return '不明';
    }
  };

  if (loading) {
    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            トレンド分析
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
          マルチタイムフレーム トレンド分析
        </Typography>

        <Grid container spacing={2}>
          {Object.entries(analyses).map(([timeframe, analysis]) => (
            <Grid item xs={12} sm={6} key={timeframe}>
              <Paper elevation={2} sx={{ p: 2 }}>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                  <Typography variant="subtitle1" fontWeight="bold">
                    {timeframe}
                  </Typography>
                  <Chip
                    label={getTrendLabel(analysis.direction)}
                    color={getTrendColor(analysis.direction) as any}
                    size="small"
                  />
                </Box>

                <Box mb={2}>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    トレンド強度: {analysis.strength.toFixed(0)}%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={analysis.strength}
                    sx={{
                      height: 8,
                      borderRadius: 4,
                      bgcolor: 'grey.200',
                      '& .MuiLinearProgress-bar': {
                        bgcolor:
                          analysis.direction === 'bullish'
                            ? 'success.main'
                            : analysis.direction === 'bearish'
                            ? 'error.main'
                            : 'warning.main',
                      },
                    }}
                  />
                </Box>

                {analysis.support_levels.length > 0 && (
                  <Box mb={1}>
                    <Typography variant="body2" color="text.secondary">
                      サポートレベル:
                    </Typography>
                    <Box display="flex" gap={1} flexWrap="wrap" mt={0.5}>
                      {analysis.support_levels.map((level, idx) => (
                        <Chip
                          key={idx}
                          label={level.toFixed(2)}
                          size="small"
                          variant="outlined"
                          color="success"
                        />
                      ))}
                    </Box>
                  </Box>
                )}

                {analysis.resistance_levels.length > 0 && (
                  <Box mb={1}>
                    <Typography variant="body2" color="text.secondary">
                      レジスタンスレベル:
                    </Typography>
                    <Box display="flex" gap={1} flexWrap="wrap" mt={0.5}>
                      {analysis.resistance_levels.map((level, idx) => (
                        <Chip
                          key={idx}
                          label={level.toFixed(2)}
                          size="small"
                          variant="outlined"
                          color="error"
                        />
                      ))}
                    </Box>
                  </Box>
                )}

                <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1 }}>
                  {analysis.description}
                </Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </CardContent>
    </Card>
  );
};

export default TrendAnalysis;
