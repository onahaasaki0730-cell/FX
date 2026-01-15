import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  LinearProgress,
} from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import TrendingFlatIcon from '@mui/icons-material/TrendingFlat';
import { marketAPI, MarketQuote } from '../services/api';

interface MarketQuoteCardProps {
  symbol: string;
}

const MarketQuoteCard: React.FC<MarketQuoteCardProps> = ({ symbol }) => {
  const [quote, setQuote] = useState<MarketQuote | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchQuote = async () => {
      try {
        const data = await marketAPI.getQuote(symbol);
        setQuote(data);
      } catch (error) {
        console.error('Failed to fetch quote:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchQuote();
    const interval = setInterval(fetchQuote, 60000); // 1分ごとに更新

    return () => clearInterval(interval);
  }, [symbol]);

  if (loading) {
    return (
      <Card>
        <CardContent>
          <LinearProgress />
        </CardContent>
      </Card>
    );
  }

  if (!quote) {
    return (
      <Card>
        <CardContent>
          <Typography>データを読み込めませんでした</Typography>
        </CardContent>
      </Card>
    );
  }

  const isPositive = (quote.change || 0) >= 0;
  const TrendIcon = isPositive ? TrendingUpIcon : TrendingDownIcon;

  return (
    <Card>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box>
            <Typography variant="h6" component="div">
              {quote.symbol}
            </Typography>
            <Typography variant="h4" component="div" sx={{ my: 1 }}>
              {quote.price.toFixed(2)}
            </Typography>
          </Box>
          <Box textAlign="right">
            <Box display="flex" alignItems="center" justifyContent="flex-end">
              <TrendIcon
                sx={{
                  color: isPositive ? 'success.main' : 'error.main',
                  mr: 0.5,
                }}
              />
              <Typography
                variant="h6"
                sx={{
                  color: isPositive ? 'success.main' : 'error.main',
                }}
              >
                {isPositive ? '+' : ''}
                {quote.change?.toFixed(2)}
              </Typography>
            </Box>
            <Typography
              variant="body2"
              sx={{
                color: isPositive ? 'success.main' : 'error.main',
              }}
            >
              {isPositive ? '+' : ''}
              {quote.change_percent?.toFixed(2)}%
            </Typography>
          </Box>
        </Box>

        <Grid container spacing={2} sx={{ mt: 1 }}>
          <Grid item xs={6}>
            <Typography variant="body2" color="text.secondary">
              高値
            </Typography>
            <Typography variant="body1">
              {quote.high?.toFixed(2) || '-'}
            </Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="body2" color="text.secondary">
              安値
            </Typography>
            <Typography variant="body1">
              {quote.low?.toFixed(2) || '-'}
            </Typography>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="body2" color="text.secondary">
              出来高
            </Typography>
            <Typography variant="body1">
              {quote.volume?.toLocaleString() || '-'}
            </Typography>
          </Grid>
        </Grid>

        <Typography
          variant="caption"
          color="text.secondary"
          sx={{ display: 'block', mt: 2 }}
        >
          更新: {new Date(quote.timestamp).toLocaleString('ja-JP')}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default MarketQuoteCard;
