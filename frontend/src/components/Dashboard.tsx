import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Grid,
  Box,
  TextField,
  Button,
  Paper,
  Tab,
  Tabs,
} from '@mui/material';
import ShowChartIcon from '@mui/icons-material/ShowChart';
import MarketQuoteCard from '../components/MarketQuoteCard';
import TrendAnalysis from '../components/TrendAnalysis';
import TradingSignal from '../components/TradingSignal';
import NewsList from '../components/NewsList';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`tabpanel-${index}`}
      aria-labelledby={`tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

const Dashboard: React.FC = () => {
  const [symbol, setSymbol] = useState('AAPL');
  const [inputSymbol, setInputSymbol] = useState('AAPL');
  const [tabValue, setTabValue] = useState(0);

  const handleSymbolChange = () => {
    if (inputSymbol.trim()) {
      setSymbol(inputSymbol.trim().toUpperCase());
    }
  };

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const timeframes = ['15m', '1h', '4h', '1d'];

  return (
    <Box sx={{ flexGrow: 1, bgcolor: 'background.default', minHeight: '100vh' }}>
      <AppBar position="static" elevation={0}>
        <Toolbar>
          <ShowChartIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Market Analysis System - リアルタイム市場分析
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        <Paper sx={{ p: 3, mb: 3 }}>
          <Box display="flex" gap={2} alignItems="center">
            <TextField
              label="銘柄シンボル"
              variant="outlined"
              value={inputSymbol}
              onChange={(e) => setInputSymbol(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  handleSymbolChange();
                }
              }}
              placeholder="例: AAPL, USDJPY, BTCUSD"
              sx={{ flexGrow: 1, maxWidth: 400 }}
            />
            <Button
              variant="contained"
              onClick={handleSymbolChange}
              size="large"
            >
              分析開始
            </Button>
          </Box>
          <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1 }}>
            推奨シンボル: AAPL (Apple), MSFT (Microsoft), GOOGL (Google), TSLA (Tesla), 
            USDJPY, EURUSD, GBPUSD, BTCUSD
          </Typography>
        </Paper>

        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
          <Tabs value={tabValue} onChange={handleTabChange}>
            <Tab label="概要" />
            <Tab label="トレンド分析" />
            <Tab label="シグナル" />
            <Tab label="ニュース" />
          </Tabs>
        </Box>

        <TabPanel value={tabValue} index={0}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <MarketQuoteCard symbol={symbol} />
            </Grid>
            <Grid item xs={12} md={8}>
              <TradingSignal symbol={symbol} timeframe="1h" />
            </Grid>
            <Grid item xs={12}>
              <TrendAnalysis symbol={symbol} timeframes={['15m', '1h', '4h', '1d']} />
            </Grid>
          </Grid>
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TrendAnalysis symbol={symbol} timeframes={timeframes} />
            </Grid>
          </Grid>
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          <Grid container spacing={3}>
            {timeframes.map((tf) => (
              <Grid item xs={12} md={6} key={tf}>
                <TradingSignal symbol={symbol} timeframe={tf} />
              </Grid>
            ))}
          </Grid>
        </TabPanel>

        <TabPanel value={tabValue} index={3}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <NewsList symbols={[symbol]} limit={20} />
            </Grid>
          </Grid>
        </TabPanel>
      </Container>
    </Box>
  );
};

export default Dashboard;
