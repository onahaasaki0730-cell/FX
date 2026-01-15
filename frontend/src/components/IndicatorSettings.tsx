import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Typography,
  Switch,
  TextField,
  FormControlLabel,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Grid,
  Divider,
  IconButton,
  Chip,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import { IndicatorSettings as IndicatorSettingsType } from '../types/indicators';

interface IndicatorSettingsProps {
  open: boolean;
  settings: IndicatorSettingsType;
  onClose: () => void;
  onSave: (settings: IndicatorSettingsType) => void;
}

const IndicatorSettings: React.FC<IndicatorSettingsProps> = ({
  open,
  settings,
  onClose,
  onSave,
}) => {
  const [localSettings, setLocalSettings] = useState<IndicatorSettingsType>(settings);

  const handleSave = () => {
    onSave(localSettings);
    onClose();
  };

  const handleReset = () => {
    setLocalSettings(settings);
  };

  const updateSetting = (
    category: keyof IndicatorSettingsType,
    key: string,
    value: any
  ) => {
    setLocalSettings((prev) => ({
      ...prev,
      [category]: {
        ...prev[category],
        [key]: value,
      },
    }));
  };

  const addPeriod = (category: 'sma' | 'ema') => {
    const periods = [...localSettings[category].periods];
    const newPeriod = periods.length > 0 ? Math.max(...periods) + 10 : 10;
    periods.push(newPeriod);
    
    const colors = [...localSettings[category].colors];
    colors.push('#' + Math.floor(Math.random() * 16777215).toString(16));

    setLocalSettings((prev) => ({
      ...prev,
      [category]: {
        ...prev[category],
        periods,
        colors,
      },
    }));
  };

  const removePeriod = (category: 'sma' | 'ema', index: number) => {
    const periods = localSettings[category].periods.filter((_, i) => i !== index);
    const colors = localSettings[category].colors.filter((_, i) => i !== index);

    setLocalSettings((prev) => ({
      ...prev,
      [category]: {
        ...prev[category],
        periods,
        colors,
      },
    }));
  };

  const updatePeriod = (category: 'sma' | 'ema', index: number, value: number) => {
    const periods = [...localSettings[category].periods];
    periods[index] = value;

    setLocalSettings((prev) => ({
      ...prev,
      [category]: {
        ...prev[category],
        periods,
      },
    }));
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>インジケーター設定</DialogTitle>
      <DialogContent dividers>
        <Box sx={{ py: 1 }}>
          {/* 移動平均線 (SMA) */}
          <Accordion defaultExpanded>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Box display="flex" alignItems="center" gap={2} width="100%">
                <Typography variant="subtitle1" fontWeight="bold">
                  単純移動平均線 (SMA)
                </Typography>
                <FormControlLabel
                  control={
                    <Switch
                      checked={localSettings.sma.enabled}
                      onChange={(e) =>
                        updateSetting('sma', 'enabled', e.target.checked)
                      }
                      onClick={(e) => e.stopPropagation()}
                    />
                  }
                  label=""
                  sx={{ ml: 'auto' }}
                />
              </Box>
            </AccordionSummary>
            <AccordionDetails>
              <Box>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  期間設定
                </Typography>
                {localSettings.sma.periods.map((period, index) => (
                  <Box key={index} display="flex" gap={1} alignItems="center" mb={1}>
                    <TextField
                      type="number"
                      label={`期間 ${index + 1}`}
                      value={period}
                      onChange={(e) =>
                        updatePeriod('sma', index, parseInt(e.target.value) || 0)
                      }
                      size="small"
                      sx={{ width: 120 }}
                    />
                    <input
                      type="color"
                      value={localSettings.sma.colors[index]}
                      onChange={(e) => {
                        const colors = [...localSettings.sma.colors];
                        colors[index] = e.target.value;
                        updateSetting('sma', 'colors', colors);
                      }}
                      style={{ width: 50, height: 40, cursor: 'pointer' }}
                    />
                    <IconButton
                      size="small"
                      onClick={() => removePeriod('sma', index)}
                      disabled={localSettings.sma.periods.length <= 1}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </Box>
                ))}
                <Button
                  startIcon={<AddIcon />}
                  onClick={() => addPeriod('sma')}
                  size="small"
                  variant="outlined"
                  sx={{ mt: 1 }}
                >
                  期間を追加
                </Button>
              </Box>
            </AccordionDetails>
          </Accordion>

          {/* 指数移動平均線 (EMA) */}
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Box display="flex" alignItems="center" gap={2} width="100%">
                <Typography variant="subtitle1" fontWeight="bold">
                  指数移動平均線 (EMA)
                </Typography>
                <FormControlLabel
                  control={
                    <Switch
                      checked={localSettings.ema.enabled}
                      onChange={(e) =>
                        updateSetting('ema', 'enabled', e.target.checked)
                      }
                      onClick={(e) => e.stopPropagation()}
                    />
                  }
                  label=""
                  sx={{ ml: 'auto' }}
                />
              </Box>
            </AccordionSummary>
            <AccordionDetails>
              <Box>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  期間設定
                </Typography>
                {localSettings.ema.periods.map((period, index) => (
                  <Box key={index} display="flex" gap={1} alignItems="center" mb={1}>
                    <TextField
                      type="number"
                      label={`期間 ${index + 1}`}
                      value={period}
                      onChange={(e) =>
                        updatePeriod('ema', index, parseInt(e.target.value) || 0)
                      }
                      size="small"
                      sx={{ width: 120 }}
                    />
                    <input
                      type="color"
                      value={localSettings.ema.colors[index]}
                      onChange={(e) => {
                        const colors = [...localSettings.ema.colors];
                        colors[index] = e.target.value;
                        updateSetting('ema', 'colors', colors);
                      }}
                      style={{ width: 50, height: 40, cursor: 'pointer' }}
                    />
                    <IconButton
                      size="small"
                      onClick={() => removePeriod('ema', index)}
                      disabled={localSettings.ema.periods.length <= 1}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </Box>
                ))}
                <Button
                  startIcon={<AddIcon />}
                  onClick={() => addPeriod('ema')}
                  size="small"
                  variant="outlined"
                  sx={{ mt: 1 }}
                >
                  期間を追加
                </Button>
              </Box>
            </AccordionDetails>
          </Accordion>

          {/* RSI */}
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Box display="flex" alignItems="center" gap={2} width="100%">
                <Typography variant="subtitle1" fontWeight="bold">
                  RSI (相対力指数)
                </Typography>
                <FormControlLabel
                  control={
                    <Switch
                      checked={localSettings.rsi.enabled}
                      onChange={(e) =>
                        updateSetting('rsi', 'enabled', e.target.checked)
                      }
                      onClick={(e) => e.stopPropagation()}
                    />
                  }
                  label=""
                  sx={{ ml: 'auto' }}
                />
              </Box>
            </AccordionSummary>
            <AccordionDetails>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={4}>
                  <TextField
                    type="number"
                    label="期間"
                    value={localSettings.rsi.period}
                    onChange={(e) =>
                      updateSetting('rsi', 'period', parseInt(e.target.value) || 14)
                    }
                    fullWidth
                    size="small"
                  />
                </Grid>
                <Grid item xs={12} sm={4}>
                  <TextField
                    type="number"
                    label="買われすぎ"
                    value={localSettings.rsi.overbought}
                    onChange={(e) =>
                      updateSetting('rsi', 'overbought', parseInt(e.target.value) || 70)
                    }
                    fullWidth
                    size="small"
                  />
                </Grid>
                <Grid item xs={12} sm={4}>
                  <TextField
                    type="number"
                    label="売られすぎ"
                    value={localSettings.rsi.oversold}
                    onChange={(e) =>
                      updateSetting('rsi', 'oversold', parseInt(e.target.value) || 30)
                    }
                    fullWidth
                    size="small"
                  />
                </Grid>
              </Grid>
            </AccordionDetails>
          </Accordion>

          {/* MACD */}
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Box display="flex" alignItems="center" gap={2} width="100%">
                <Typography variant="subtitle1" fontWeight="bold">
                  MACD
                </Typography>
                <FormControlLabel
                  control={
                    <Switch
                      checked={localSettings.macd.enabled}
                      onChange={(e) =>
                        updateSetting('macd', 'enabled', e.target.checked)
                      }
                      onClick={(e) => e.stopPropagation()}
                    />
                  }
                  label=""
                  sx={{ ml: 'auto' }}
                />
              </Box>
            </AccordionSummary>
            <AccordionDetails>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={4}>
                  <TextField
                    type="number"
                    label="高速期間"
                    value={localSettings.macd.fastPeriod}
                    onChange={(e) =>
                      updateSetting('macd', 'fastPeriod', parseInt(e.target.value) || 12)
                    }
                    fullWidth
                    size="small"
                  />
                </Grid>
                <Grid item xs={12} sm={4}>
                  <TextField
                    type="number"
                    label="低速期間"
                    value={localSettings.macd.slowPeriod}
                    onChange={(e) =>
                      updateSetting('macd', 'slowPeriod', parseInt(e.target.value) || 26)
                    }
                    fullWidth
                    size="small"
                  />
                </Grid>
                <Grid item xs={12} sm={4}>
                  <TextField
                    type="number"
                    label="シグナル期間"
                    value={localSettings.macd.signalPeriod}
                    onChange={(e) =>
                      updateSetting(
                        'macd',
                        'signalPeriod',
                        parseInt(e.target.value) || 9
                      )
                    }
                    fullWidth
                    size="small"
                  />
                </Grid>
              </Grid>
            </AccordionDetails>
          </Accordion>

          {/* ストキャスティクス */}
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Box display="flex" alignItems="center" gap={2} width="100%">
                <Typography variant="subtitle1" fontWeight="bold">
                  ストキャスティクス
                </Typography>
                <FormControlLabel
                  control={
                    <Switch
                      checked={localSettings.stochastic.enabled}
                      onChange={(e) =>
                        updateSetting('stochastic', 'enabled', e.target.checked)
                      }
                      onClick={(e) => e.stopPropagation()}
                    />
                  }
                  label=""
                  sx={{ ml: 'auto' }}
                />
              </Box>
            </AccordionSummary>
            <AccordionDetails>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={3}>
                  <TextField
                    type="number"
                    label="%K期間"
                    value={localSettings.stochastic.kPeriod}
                    onChange={(e) =>
                      updateSetting(
                        'stochastic',
                        'kPeriod',
                        parseInt(e.target.value) || 14
                      )
                    }
                    fullWidth
                    size="small"
                  />
                </Grid>
                <Grid item xs={12} sm={3}>
                  <TextField
                    type="number"
                    label="%D期間"
                    value={localSettings.stochastic.dPeriod}
                    onChange={(e) =>
                      updateSetting(
                        'stochastic',
                        'dPeriod',
                        parseInt(e.target.value) || 3
                      )
                    }
                    fullWidth
                    size="small"
                  />
                </Grid>
                <Grid item xs={12} sm={3}>
                  <TextField
                    type="number"
                    label="買われすぎ"
                    value={localSettings.stochastic.overbought}
                    onChange={(e) =>
                      updateSetting(
                        'stochastic',
                        'overbought',
                        parseInt(e.target.value) || 80
                      )
                    }
                    fullWidth
                    size="small"
                  />
                </Grid>
                <Grid item xs={12} sm={3}>
                  <TextField
                    type="number"
                    label="売られすぎ"
                    value={localSettings.stochastic.oversold}
                    onChange={(e) =>
                      updateSetting(
                        'stochastic',
                        'oversold',
                        parseInt(e.target.value) || 20
                      )
                    }
                    fullWidth
                    size="small"
                  />
                </Grid>
              </Grid>
            </AccordionDetails>
          </Accordion>

          {/* ボリンジャーバンド */}
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Box display="flex" alignItems="center" gap={2} width="100%">
                <Typography variant="subtitle1" fontWeight="bold">
                  ボリンジャーバンド
                </Typography>
                <FormControlLabel
                  control={
                    <Switch
                      checked={localSettings.bollingerBands.enabled}
                      onChange={(e) =>
                        updateSetting('bollingerBands', 'enabled', e.target.checked)
                      }
                      onClick={(e) => e.stopPropagation()}
                    />
                  }
                  label=""
                  sx={{ ml: 'auto' }}
                />
              </Box>
            </AccordionSummary>
            <AccordionDetails>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    type="number"
                    label="期間"
                    value={localSettings.bollingerBands.period}
                    onChange={(e) =>
                      updateSetting(
                        'bollingerBands',
                        'period',
                        parseInt(e.target.value) || 20
                      )
                    }
                    fullWidth
                    size="small"
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    type="number"
                    label="標準偏差"
                    value={localSettings.bollingerBands.stdDev}
                    onChange={(e) =>
                      updateSetting(
                        'bollingerBands',
                        'stdDev',
                        parseFloat(e.target.value) || 2
                      )
                    }
                    fullWidth
                    size="small"
                    inputProps={{ step: 0.1 }}
                  />
                </Grid>
              </Grid>
            </AccordionDetails>
          </Accordion>

          {/* ATR */}
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Box display="flex" alignItems="center" gap={2} width="100%">
                <Typography variant="subtitle1" fontWeight="bold">
                  ATR (平均真の範囲)
                </Typography>
                <FormControlLabel
                  control={
                    <Switch
                      checked={localSettings.atr.enabled}
                      onChange={(e) =>
                        updateSetting('atr', 'enabled', e.target.checked)
                      }
                      onClick={(e) => e.stopPropagation()}
                    />
                  }
                  label=""
                  sx={{ ml: 'auto' }}
                />
              </Box>
            </AccordionSummary>
            <AccordionDetails>
              <TextField
                type="number"
                label="期間"
                value={localSettings.atr.period}
                onChange={(e) =>
                  updateSetting('atr', 'period', parseInt(e.target.value) || 14)
                }
                fullWidth
                size="small"
              />
            </AccordionDetails>
          </Accordion>

          {/* 出来高 */}
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Box display="flex" alignItems="center" gap={2} width="100%">
                <Typography variant="subtitle1" fontWeight="bold">
                  出来高
                </Typography>
                <FormControlLabel
                  control={
                    <Switch
                      checked={localSettings.volume.enabled}
                      onChange={(e) =>
                        updateSetting('volume', 'enabled', e.target.checked)
                      }
                      onClick={(e) => e.stopPropagation()}
                    />
                  }
                  label=""
                  sx={{ ml: 'auto' }}
                />
              </Box>
            </AccordionSummary>
          </Accordion>

          {/* OBV */}
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Box display="flex" alignItems="center" gap={2} width="100%">
                <Typography variant="subtitle1" fontWeight="bold">
                  OBV (オンバランスボリューム)
                </Typography>
                <FormControlLabel
                  control={
                    <Switch
                      checked={localSettings.obv.enabled}
                      onChange={(e) =>
                        updateSetting('obv', 'enabled', e.target.checked)
                      }
                      onClick={(e) => e.stopPropagation()}
                    />
                  }
                  label=""
                  sx={{ ml: 'auto' }}
                />
              </Box>
            </AccordionSummary>
          </Accordion>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleReset} color="inherit">
          リセット
        </Button>
        <Button onClick={onClose} color="inherit">
          キャンセル
        </Button>
        <Button onClick={handleSave} variant="contained" color="primary">
          保存
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default IndicatorSettings;
