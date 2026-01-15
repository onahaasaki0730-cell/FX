import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  IconButton,
  Paper,
  Tooltip,
  Chip,
} from '@mui/material';
import ZoomOutMapIcon from '@mui/icons-material/ZoomOutMap';
import CloseFullscreenIcon from '@mui/icons-material/CloseFullscreen';
import SettingsIcon from '@mui/icons-material/Settings';
import { IndicatorSettings as IndicatorSettingsType } from '../types/indicators';

interface ChartData {
  timeframe: string;
  trend: string;
  strength: number;
  price: number;
}

interface MultiChartViewProps {
  symbol: string;
  timeframes: string[];
  chartData: Record<string, ChartData>;
  indicatorSettings: IndicatorSettingsType;
  onOpenSettings: () => void;
}

const MultiChartView: React.FC<MultiChartViewProps> = ({
  symbol,
  timeframes,
  chartData,
  indicatorSettings,
  onOpenSettings,
}) => {
  const [expandedTimeframe, setExpandedTimeframe] = useState<string | null>(null);

  const handleChartClick = (timeframe: string) => {
    if (expandedTimeframe === timeframe) {
      setExpandedTimeframe(null);
    } else {
      setExpandedTimeframe(timeframe);
    }
  };

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'bullish':
        return '#4CAF50';
      case 'bearish':
        return '#f44336';
      case 'sideways':
        return '#FF9800';
      default:
        return '#9E9E9E';
    }
  };

  const getTrendLabel = (trend: string) => {
    switch (trend) {
      case 'bullish':
        return '上昇';
      case 'bearish':
        return '下降';
      case 'sideways':
        return 'レンジ';
      default:
        return '-';
    }
  };

  // チャートのプレースホルダーコンポーネント
  const ChartPlaceholder: React.FC<{
    timeframe: string;
    isExpanded: boolean;
    isSmall: boolean;
  }> = ({ timeframe, isExpanded, isSmall }) => {
    const data = chartData[timeframe];
    const trendColor = data ? getTrendColor(data.trend) : '#9E9E9E';

    return (
      <Paper
        elevation={isExpanded ? 4 : 2}
        sx={{
          height: '100%',
          position: 'relative',
          cursor: 'pointer',
          transition: 'all 0.3s ease',
          border: isExpanded ? `3px solid ${trendColor}` : '1px solid #e0e0e0',
          '&:hover': {
            elevation: 6,
            transform: 'scale(1.02)',
          },
          overflow: 'hidden',
        }}
        onClick={() => handleChartClick(timeframe)}
      >
        <Box
          sx={{
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            bgcolor: '#1a1a1a',
            color: 'white',
            p: isSmall ? 1 : 2,
          }}
        >
          {/* ヘッダー */}
          <Box
            display="flex"
            justifyContent="space-between"
            alignItems="center"
            mb={isSmall ? 0.5 : 1}
          >
            <Box display="flex" alignItems="center" gap={1}>
              <Typography
                variant={isSmall ? 'caption' : 'subtitle1'}
                fontWeight="bold"
              >
                {timeframe}
              </Typography>
              {data && (
                <Chip
                  label={getTrendLabel(data.trend)}
                  size="small"
                  sx={{
                    bgcolor: trendColor,
                    color: 'white',
                    fontSize: isSmall ? '0.65rem' : '0.75rem',
                    height: isSmall ? 16 : 24,
                  }}
                />
              )}
            </Box>
            <Tooltip title={isExpanded ? '通常表示に戻す' : '拡大表示'}>
              <IconButton size="small" sx={{ color: 'white' }}>
                {isExpanded ? (
                  <CloseFullscreenIcon fontSize={isSmall ? 'small' : 'medium'} />
                ) : (
                  <ZoomOutMapIcon fontSize={isSmall ? 'small' : 'medium'} />
                )}
              </IconButton>
            </Tooltip>
          </Box>

          {/* 価格情報 */}
          {data && !isSmall && (
            <Box mb={1}>
              <Typography variant="h6" fontWeight="bold">
                {data.price.toFixed(2)}
              </Typography>
              <Typography variant="caption" color="rgba(255,255,255,0.7)">
                強度: {data.strength.toFixed(0)}%
              </Typography>
            </Box>
          )}

          {/* チャートエリア（プレースホルダー） */}
          <Box
            sx={{
              flex: 1,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              bgcolor: 'rgba(255,255,255,0.05)',
              borderRadius: 1,
              position: 'relative',
              minHeight: isSmall ? 80 : 200,
            }}
          >
            {/* グリッド線のシミュレーション */}
            <Box
              sx={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                backgroundImage: `
                  linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
                  linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)
                `,
                backgroundSize: isSmall ? '20px 20px' : '40px 40px',
              }}
            />

            {/* 簡易的なローソク足表示 */}
            <Box
              sx={{
                display: 'flex',
                alignItems: 'flex-end',
                gap: isSmall ? 0.25 : 0.5,
                height: '80%',
                position: 'relative',
                zIndex: 1,
              }}
            >
              {[...Array(isSmall ? 10 : 20)].map((_, i) => {
                const height = Math.random() * 80 + 20;
                const isGreen = Math.random() > 0.5;
                return (
                  <Box
                    key={i}
                    sx={{
                      width: isSmall ? 4 : 8,
                      height: `${height}%`,
                      bgcolor: isGreen ? '#4CAF50' : '#f44336',
                      opacity: 0.7,
                      borderRadius: 0.5,
                    }}
                  />
                );
              })}
            </Box>

            {/* 移動平均線のシミュレーション */}
            {indicatorSettings.sma.enabled && (
              <svg
                style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: '100%',
                  pointerEvents: 'none',
                }}
              >
                {indicatorSettings.sma.periods.map((_, index) => (
                  <path
                    key={index}
                    d={`M 0,${50 + index * 10} Q 50,${30 + index * 10} 100,${
                      50 + index * 10
                    } T 200,${50 + index * 10} T 300,${50 + index * 10}`}
                    fill="none"
                    stroke={indicatorSettings.sma.colors[index]}
                    strokeWidth="2"
                    opacity="0.7"
                  />
                ))}
              </svg>
            )}

            <Typography
              variant={isSmall ? 'caption' : 'body2'}
              color="rgba(255,255,255,0.5)"
              sx={{ position: 'absolute' }}
            >
              {symbol} チャート
            </Typography>
          </Box>

          {/* インジケーター情報（小さい表示では非表示） */}
          {!isSmall && (
            <Box mt={1}>
              <Typography variant="caption" color="rgba(255,255,255,0.6)">
                有効なインジケーター:{' '}
                {Object.entries(indicatorSettings)
                  .filter(([_, value]) => value.enabled)
                  .map(([key]) => key.toUpperCase())
                  .join(', ') || 'なし'}
              </Typography>
            </Box>
          )}
        </Box>
      </Paper>
    );
  };

  // 拡大表示モード
  if (expandedTimeframe) {
    const otherTimeframes = timeframes.filter((tf) => tf !== expandedTimeframe);

    return (
      <Card>
        <CardContent sx={{ p: 2 }}>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
            <Typography variant="h6">
              {symbol} - マルチタイムフレームチャート
            </Typography>
            <Tooltip title="インジケーター設定">
              <IconButton onClick={onOpenSettings} size="small">
                <SettingsIcon />
              </IconButton>
            </Tooltip>
          </Box>

          <Box display="flex" gap={2} height="600px">
            {/* メインチャート（拡大表示） */}
            <Box flex={1} minWidth={0}>
              <ChartPlaceholder
                timeframe={expandedTimeframe}
                isExpanded={true}
                isSmall={false}
              />
            </Box>

            {/* サイドバー（他の時間足） */}
            <Box
              sx={{
                width: 200,
                display: 'flex',
                flexDirection: 'column',
                gap: 2,
              }}
            >
              {otherTimeframes.map((tf) => (
                <Box key={tf} height="33.33%">
                  <ChartPlaceholder
                    timeframe={tf}
                    isExpanded={false}
                    isSmall={true}
                  />
                </Box>
              ))}
            </Box>
          </Box>
        </CardContent>
      </Card>
    );
  }

  // 通常表示モード（2x2グリッド）
  return (
    <Card>
      <CardContent sx={{ p: 2 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6">
            {symbol} - マルチタイムフレームチャート
          </Typography>
          <Tooltip title="インジケーター設定">
            <IconButton onClick={onOpenSettings} size="small">
              <SettingsIcon />
            </IconButton>
          </Tooltip>
        </Box>

        <Box
          display="grid"
          gridTemplateColumns="repeat(2, 1fr)"
          gap={2}
          sx={{
            '@media (max-width: 900px)': {
              gridTemplateColumns: '1fr',
            },
          }}
        >
          {timeframes.map((tf) => (
            <Box key={tf} height="300px">
              <ChartPlaceholder timeframe={tf} isExpanded={false} isSmall={false} />
            </Box>
          ))}
        </Box>

        <Box mt={2}>
          <Typography variant="caption" color="text.secondary">
            ヒント: チャートをクリックすると拡大表示できます
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default MultiChartView;
