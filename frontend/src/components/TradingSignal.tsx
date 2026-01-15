import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  LinearProgress,
  Paper,
  Grid,
} from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import TrendingFlatIcon from '@mui/icons-material/TrendingFlat';
import { marketAPI, TradingSignal as TradingSignalType } from '../services/api';

interface TradingSignalProps {
  symbol: string;
  timeframe: string;
}

const TradingSignal: React.FC<TradingSignalProps> = ({ symbol, timeframe }) => {
  const [signal, setSignal] = useState<TradingSignalType | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSignal = async () => {
      try {
        const data = await marketAPI.getTradingSignal(symbol, timeframe);
        setSignal(data);
      } catch (error) {
        console.error('Failed to fetch trading signal:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchSignal();
    const interval = setInterval(fetchSignal, 300000); // 5分ごとに更新

    return () => clearInterval(interval);
  }, [symbol, timeframe]);

  const getSignalColor = (signalType: string) => {
    switch (signalType) {
      case 'strong_buy':
        return 'success';
      case 'buy':
        return 'success';
      case 'sell':
        return 'error';
      case 'strong_sell':
        return 'error';
      default:
        return 'default';
    }
  };

  const getSignalLabel = (signalType: string) => {
    switch (signalType) {
      case 'strong_buy':
        return '強い買い';
      case 'buy':
        return '買い';
      case 'neutral':
        return '中立';
      case 'sell':
        return '売り';
      case 'strong_sell':
        return '強い売り';
      default:
        return '不明';
    }
  };

  const getSignalIcon = (signalType: string) => {
    if (signalType.includes('buy')) return TrendingUpIcon;
    if (signalType.includes('sell')) return TrendingDownIcon;
    return TrendingFlatIcon;
  };

  if (loading) {
    return (
      <Card>
        <CardContent>
          <LinearProgress />
        </CardContent>
      </Card>
    );
  }

  if (!signal) {
    return (
      <Card>
        <CardContent>
          <Typography>シグナルを読み込めませんでした</Typography>
        </CardContent>
      </Card>
    );
  }

  const SignalIcon = getSignalIcon(signal.signal);

  return (
    <Card>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Box>
            <Typography variant="h6" gutterBottom>
              トレーディングシグナル
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {symbol} • {timeframe}
            </Typography>
          </Box>
          <Box display="flex" alignItems="center">
            <SignalIcon
              sx={{
                fontSize: 40,
                color:
                  signal.signal.includes('buy')
                    ? 'success.main'
                    : signal.signal.includes('sell')
                    ? 'error.main'
                    : 'text.secondary',
              }}
            />
          </Box>
        </Box>

        <Box mb={3}>
          <Box display="flex" alignItems="center" justifyContent="space-between" mb={1}>
            <Chip
              label={getSignalLabel(signal.signal)}
              color={getSignalColor(signal.signal) as any}
              size="large"
              sx={{ fontSize: '1rem', fontWeight: 'bold', px: 2 }}
            />
            <Typography variant="h6" color="text.secondary">
              信頼度: {signal.confidence.toFixed(0)}%
            </Typography>
          </Box>
          <LinearProgress
            variant="determinate"
            value={signal.confidence}
            sx={{
              height: 8,
              borderRadius: 4,
              mt: 1,
              bgcolor: 'grey.200',
            }}
          />
        </Box>

        {(signal.entry_price || signal.stop_loss || signal.take_profit) && (
          <Grid container spacing={2} mb={2}>
            {signal.entry_price && (
              <Grid item xs={4}>
                <Paper elevation={0} sx={{ p: 1.5, bgcolor: 'primary.50' }}>
                  <Typography variant="caption" color="text.secondary">
                    エントリー
                  </Typography>
                  <Typography variant="h6">{signal.entry_price.toFixed(2)}</Typography>
                </Paper>
              </Grid>
            )}
            {signal.stop_loss && (
              <Grid item xs={4}>
                <Paper elevation={0} sx={{ p: 1.5, bgcolor: 'error.50' }}>
                  <Typography variant="caption" color="text.secondary">
                    ストップロス
                  </Typography>
                  <Typography variant="h6">{signal.stop_loss.toFixed(2)}</Typography>
                </Paper>
              </Grid>
            )}
            {signal.take_profit && (
              <Grid item xs={4}>
                <Paper elevation={0} sx={{ p: 1.5, bgcolor: 'success.50' }}>
                  <Typography variant="caption" color="text.secondary">
                    利確
                  </Typography>
                  <Typography variant="h6">{signal.take_profit.toFixed(2)}</Typography>
                </Paper>
              </Grid>
            )}
          </Grid>
        )}

        {signal.reasons.length > 0 && (
          <Box>
            <Typography variant="subtitle2" gutterBottom>
              シグナルの根拠:
            </Typography>
            <Box component="ul" sx={{ pl: 2, mt: 1 }}>
              {signal.reasons.map((reason, index) => (
                <Typography
                  component="li"
                  key={index}
                  variant="body2"
                  color="text.secondary"
                  sx={{ mb: 0.5 }}
                >
                  {reason}
                </Typography>
              ))}
            </Box>
          </Box>
        )}

        <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 2 }}>
          更新: {new Date(signal.timestamp).toLocaleString('ja-JP')}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default TradingSignal;
