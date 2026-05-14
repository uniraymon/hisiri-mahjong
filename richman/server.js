// 大富翁遊戲伺服器 - Node.js + Socket.io
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: '*' } });

app.use(express.static(path.join(__dirname, 'public')));

// ===== 常數 =====
const STAMINA_REGEN_MS = 5 * 60 * 1000; // 5分鐘回1體力（測試可改 30 * 1000）
const MAX_STAMINA = 5;
const INITIAL_MONEY = 15000;
const PASS_START_BONUS = 2000;
const BOARD_SIZE = 200;
const PLAYER_COLORS = ['#E74C3C','#3498DB','#2ECC71','#F39C12','#9B59B6','#E67E22'];
const MAX_PROPERTY_LEVEL = 4;

// ===== 地圖建置 =====
function buildBoard() {
  const board = Array.from({ length: BOARD_SIZE }, (_, i) => ({
    position: i, type: 'empty', name: '空地', color: '#BDC3C7', textColor: '#333'
  }));

  // 固定特殊格
  board[0]   = { position: 0,   type: 'start',        name: '起點',     color: '#27AE60', textColor: '#fff', bonus: PASS_START_BONUS };
  board[50]  = { position: 50,  type: 'jail',          name: '監獄',     color: '#7F8C8D', textColor: '#fff' };
  board[100] = { position: 100, type: 'free_parking',  name: '免費停車', color: '#8E44AD', textColor: '#fff' };
  board[150] = { position: 150, type: 'go_to_jail',    name: '去坐牢',   color: '#C0392B', textColor: '#fff' };

  // 事件格配置
  const eventMap = {
    chance:       [7,17,22,32,42,57,67,72,82,92,107,117,122,132,142,157,167,172,182,192],
    chest:        [12,27,37,52,62,77,87,102,112,127,137,152,162,177,187],
    tax:          [4,24,44,64,84,104,124,144,164,184],
    casino:       [38,63,88,138,188],
    hospital:     [25,75,125,175],
    stock_market: [15,65,115,165],
    bank_square:  [35,85,135,185],
    airport:      [48,98,148,198],
  };
  const eventDefs = {
    chance:       { name: '命運',     color: '#E67E22', textColor: '#fff' },
    chest:        { name: '福利',     color: '#3498DB', textColor: '#fff' },
    tax:          { name: '稅務局',   color: '#E74C3C', textColor: '#fff', amount: 1000 },
    casino:       { name: '賭場',     color: '#F39C12', textColor: '#fff' },
    hospital:     { name: '醫院',     color: '#E91E63', textColor: '#fff', fee: 1500 },
    stock_market: { name: '股票市場', color: '#1ABC9C', textColor: '#fff' },
    bank_square:  { name: '銀行',     color: '#2ECC71', textColor: '#fff' },
    airport:      { name: '機場',     color: '#5DADE2', textColor: '#fff', fee: 500 },
  };
  Object.entries(eventMap).forEach(([type, positions]) => {
    positions.forEach(p => { board[p] = { position: p, type, ...eventDefs[type] }; });
  });

  // 地產群組（8組各15筆 = 120個地產）
  const groups = [
    { name: '台北市', color: '#8B4513', textColor: '#fff', props: [
      ['台北車站',800],['忠孝東路',850],['信義計畫',900],['仁愛路',950],['敦化南路',1000],
      ['南京東路',1050],['和平東路',1050],['長安東路',1100],['光復南路',1100],['市民大道',1150],
      ['新生南路',1150],['羅斯福路',1200],['大安路',1200],['文山大道',1250],['木柵路',1250] ]},
    { name: '新北市', color: '#C0392B', textColor: '#fff', props: [
      ['板橋大道',1400],['新莊路',1450],['三重街',1500],['蘆洲路',1500],['永和街',1550],
      ['中和路',1550],['土城街',1600],['新店路',1600],['淡水大道',1650],['汐止路',1700],
      ['瑞芳街',1700],['平溪路',1750],['深坑街',1750],['烏來路',1800],['石碇大道',1800] ]},
    { name: '桃竹苗', color: '#9B59B6', textColor: '#fff', props: [
      ['桃園大道',2000],['中壢路',2050],['楊梅街',2100],['龜山路',2100],['平鎮大道',2150],
      ['新竹大道',2200],['竹北路',2250],['新豐街',2250],['苗栗路',2300],['頭份街',2350],
      ['公館路',2350],['三義大道',2400],['南庄街',2400],['獅潭路',2450],['造橋大道',2450] ]},
    { name: '台中市', color: '#2980B9', textColor: '#fff', props: [
      ['台中大道',2800],['西屯路',2850],['北屯街',2900],['南屯路',2900],['烏日大道',2950],
      ['霧峰路',3000],['大里街',3050],['太平路',3050],['豐原大道',3100],['東勢路',3150],
      ['神岡街',3150],['清水路',3200],['梧棲大道',3200],['大肚街',3250],['龍井路',3250] ]},
    { name: '彰雲嘉', color: '#27AE60', textColor: '#fff', props: [
      ['彰化大道',3600],['員林路',3650],['溪湖街',3700],['北斗路',3700],['南投大道',3750],
      ['草屯路',3800],['埔里街',3850],['集集路',3850],['雲林大道',3900],['斗六路',3950],
      ['北港街',3950],['嘉義大道',4000],['民雄路',4050],['朴子街',4050],['布袋路',4100] ]},
    { name: '台南高雄', color: '#D4AC0D', textColor: '#fff', props: [
      ['台南大道',4500],['安平路',4550],['新化街',4600],['永康路',4600],['高雄大道',4700],
      ['左營路',4750],['三民街',4800],['鳳山路',4800],['苓雅大道',4850],['前金路',4900],
      ['旗津街',4950],['林園路',4950],['屏東大道',5000],['潮州路',5050],['恆春大道',5100] ]},
    { name: '東亞', color: '#E67E22', textColor: '#fff', props: [
      ['東京大道',6000],['大阪路',6100],['京都街',6200],['名古屋路',6200],['橫濱大道',6300],
      ['首爾路',6400],['釜山街',6500],['濟州路',6500],['香港大道',6600],['澳門路',6700],
      ['廣州街',6700],['上海路',6800],['北京大道',7000],['深圳路',7000],['成都大道',7100] ]},
    { name: '歐美', color: '#E74C3C', textColor: '#fff', props: [
      ['紐約大道',8500],['洛杉磯路',8600],['芝加哥街',8700],['休士頓路',8800],['舊金山大道',9000],
      ['倫敦路',9200],['巴黎街',9400],['柏林路',9400],['羅馬大道',9600],['馬德里路',9800],
      ['阿姆斯特丹街',10000],['維也納路',10200],['蘇黎世大道',10500],['盧森堡路',11000],['摩納哥大道',12000] ]},
  ];

  // 把地產填入空格（按順序）
  const emptyPositions = board.filter(sq => sq.type === 'empty').map(sq => sq.position);
  let pi = 0;
  groups.forEach((group, gi) => {
    group.props.forEach(([name, price]) => {
      if (pi < emptyPositions.length) {
        const pos = emptyPositions[pi++];
        board[pos] = {
          position: pos, type: 'property',
          name, groupName: group.name, groupIdx: gi,
          color: group.color, textColor: group.textColor,
          price, rentBase: Math.floor(price * 0.1),
          upgradeCost: Math.floor(price * 0.5),
        };
      }
    });
  });

  return board;
}

// ===== 股票初始化 =====
function initStocks() {
  return {
    TECH: { id: 'TECH', name: '科技股', price: 100, base: 100, volatility: 0.15 },
    FOOD: { id: 'FOOD', name: '食品股', price: 80,  base: 80,  volatility: 0.08 },
    CONS: { id: 'CONS', name: '建設股', price: 120, base: 120, volatility: 0.10 },
    SHIP: { id: 'SHIP', name: '航運股', price: 60,  base: 60,  volatility: 0.12 },
    ENER: { id: 'ENER', name: '能源股', price: 150, base: 150, volatility: 0.09 },
  };
}

// ===== 打工任務初始化 =====
function initJobs() {
  return [
    { id: 'j1', name: '送報紙',       pay: 500,  cooldown: 10 * 60 * 1000, lastDone: {} },
    { id: 'j2', name: '餐廳服務生',   pay: 800,  cooldown: 15 * 60 * 1000, lastDone: {} },
    { id: 'j3', name: '便利商店打工', pay: 600,  cooldown: 12 * 60 * 1000, lastDone: {} },
    { id: 'j4', name: '計程車司機',   pay: 700,  cooldown: 15 * 60 * 1000, lastDone: {} },
    { id: 'j5', name: '家庭教師',     pay: 1000, cooldown: 20 * 60 * 1000, lastDone: {} },
    { id: 'j6', name: '工廠作業員',   pay: 750,  cooldown: 15 * 60 * 1000, lastDone: {} },
    { id: 'j7', name: '超市收銀員',   pay: 650,  cooldown: 12 * 60 * 1000, lastDone: {} },
    { id: 'j8', name: '倉庫管理員',   pay: 900,  cooldown: 18 * 60 * 1000, lastDone: {} },
  ];
}

// ===== 命運/福利卡 =====
const CHANCE_CARDS = [
  { text: '中了彩券！獲得 $3000', effect: (p) => { p.money += 3000; return `${p.name} 中彩券 +$3000`; } },
  { text: '繳交所得稅 $800',      effect: (p) => { p.money -= 800;  return `${p.name} 繳稅 -$800`; } },
  { text: '投資獲利 $1500',       effect: (p) => { p.money += 1500; return `${p.name} 投資獲利 +$1500`; } },
  { text: '房屋修繕費 $1000',     effect: (p) => { p.money -= 1000; return `${p.name} 修繕費 -$1000`; } },
  { text: '股市大漲，獲利 $2000', effect: (p) => { p.money += 2000; return `${p.name} 股市大漲 +$2000`; } },
  { text: '被罰款 $500',          effect: (p) => { p.money -= 500;  return `${p.name} 被罰款 -$500`; } },
  { text: '獲得遺產 $5000',       effect: (p) => { p.money += 5000; return `${p.name} 獲遺產 +$5000`; } },
  { text: '醫療費用 $1200',       effect: (p) => { p.money -= 1200; return `${p.name} 醫療費 -$1200`; } },
  { text: '前進3格',              effect: (p, g) => { movePlayer(p, 3, g, true); return `${p.name} 前進3格`; } },
  { text: '後退3格',              effect: (p, g) => { movePlayer(p, -3, g, true); return `${p.name} 後退3格`; } },
  { text: '直接前往起點，收取過路費', effect: (p, g) => { p.money += PASS_START_BONUS; p.position = 0; return `${p.name} 回到起點 +$${PASS_START_BONUS}`; } },
  { text: '去坐牢！',             effect: (p) => { p.position = 50; p.jailTurns = 3; return `${p.name} 被送進監獄`; } },
];
const CHEST_CARDS = [
  { text: '薪水入帳 $2000',       effect: (p) => { p.money += 2000; return `${p.name} 薪水 +$2000`; } },
  { text: '政府補貼 $800',        effect: (p) => { p.money += 800;  return `${p.name} 補貼 +$800`; } },
  { text: '繳交保險費 $600',      effect: (p) => { p.money -= 600;  return `${p.name} 保費 -$600`; } },
  { text: '生日快樂！獲得 $1000', effect: (p) => { p.money += 1000; return `${p.name} 生日快樂 +$1000`; } },
  { text: '銀行錯誤，退款 $300',  effect: (p) => { p.money += 300;  return `${p.name} 銀行退款 +$300`; } },
  { text: '繳交水電費 $400',      effect: (p) => { p.money -= 400;  return `${p.name} 水電費 -$400`; } },
  { text: '競賽獎金 $1500',       effect: (p) => { p.money += 1500; return `${p.name} 競賽獎金 +$1500`; } },
  { text: '罰款通知 $700',        effect: (p) => { p.money -= 700;  return `${p.name} 罰款 -$700`; } },
];

// ===== 遊戲狀態 =====
const BOARD = buildBoard();
let game = createGame();

function createGame() {
  return {
    status: 'waiting',
    players: {},
    properties: {},  // position -> { ownerId, level }
    stocks: initStocks(),
    jobs: initJobs(),
    log: [],
    colorIndex: 0,
  };
}

function addLog(msg) {
  game.log.unshift({ msg, time: Date.now() });
  if (game.log.length > 50) game.log.pop();
  io.emit('log', { msg, time: Date.now() });
}

function broadcastState() {
  io.emit('game_state', buildClientState());
}

function buildClientState() {
  return {
    status: game.status,
    players: Object.values(game.players).map(p => ({
      id: p.id, name: p.name, color: p.color,
      money: p.money, position: p.position,
      stamina: calcStamina(p), maxStamina: MAX_STAMINA,
      bankDeposit: p.bankDeposit,
      stocks: p.stocks,
      jailTurns: p.jailTurns,
      isBankrupt: p.isBankrupt,
      properties: Object.entries(game.properties)
        .filter(([, v]) => v.ownerId === p.id)
        .map(([pos]) => Number(pos)),
    })),
    properties: game.properties,
    stocks: game.stocks,
    log: game.log.slice(0, 20),
  };
}

// ===== 體力計算 =====
function calcStamina(player) {
  const now = Date.now();
  const elapsed = now - player.lastStaminaTime;
  const regens = Math.floor(elapsed / STAMINA_REGEN_MS);
  return Math.min(MAX_STAMINA, player.stamina + regens);
}

function consumeStamina(player) {
  const now = Date.now();
  const elapsed = now - player.lastStaminaTime;
  const regens = Math.floor(elapsed / STAMINA_REGEN_MS);
  player.stamina = Math.min(MAX_STAMINA, player.stamina + regens) - 1;
  if (regens > 0) player.lastStaminaTime += regens * STAMINA_REGEN_MS;
  if (player.stamina < 0) player.stamina = 0;
}

// ===== 移動邏輯 =====
function movePlayer(player, steps, silent = false) {
  const oldPos = player.position;
  let newPos = ((player.position + steps) % BOARD_SIZE + BOARD_SIZE) % BOARD_SIZE;

  // 過起點給獎金
  if (steps > 0 && newPos < oldPos && !silent) {
    player.money += PASS_START_BONUS;
    addLog(`🏠 ${player.name} 經過起點，獲得 $${PASS_START_BONUS}`);
  }
  player.position = newPos;
}

function handleLanding(player) {
  const sq = BOARD[player.position];
  let msg = `${player.name} 停在「${sq.name}」(${player.position})`;

  switch (sq.type) {
    case 'start':
      player.money += sq.bonus;
      msg += ` → 獲得 $${sq.bonus}`;
      break;

    case 'property': {
      const prop = game.properties[sq.position];
      if (!prop) {
        // 可以購買
        io.to(player.id).emit('can_buy', { position: sq.position, price: sq.price, name: sq.name });
        msg += ` → 可購買（$${sq.price}）`;
      } else if (prop.ownerId === player.id) {
        msg += ` → 自己的地產`;
      } else {
        const owner = game.players[prop.ownerId];
        if (owner && !owner.isBankrupt) {
          const rent = calcRent(sq, prop.level);
          player.money -= rent;
          owner.money += rent;
          msg += ` → 支付租金 $${rent} 給 ${owner.name}`;
          checkBankruptcy(player);
        }
      }
      break;
    }

    case 'chance': {
      const card = CHANCE_CARDS[Math.floor(Math.random() * CHANCE_CARDS.length)];
      const result = card.effect(player, game);
      msg += ` → ${card.text}（${result}）`;
      checkBankruptcy(player);
      break;
    }

    case 'chest': {
      const card = CHEST_CARDS[Math.floor(Math.random() * CHEST_CARDS.length)];
      const result = card.effect(player, game);
      msg += ` → ${card.text}（${result}）`;
      checkBankruptcy(player);
      break;
    }

    case 'tax':
      player.money -= sq.amount;
      msg += ` → 繳稅 $${sq.amount}`;
      checkBankruptcy(player);
      break;

    case 'go_to_jail':
      player.position = 50;
      player.jailTurns = 3;
      msg += ` → 被抓進監獄！`;
      break;

    case 'hospital':
      player.money -= sq.fee;
      msg += ` → 醫療費 $${sq.fee}`;
      checkBankruptcy(player);
      break;

    case 'airport':
      player.money -= sq.fee;
      msg += ` → 機場費 $${sq.fee}`;
      break;

    case 'casino':
      msg += ` → 到了賭場！可以玩小遊戲`;
      io.to(player.id).emit('casino_arrive', {});
      break;

    case 'stock_market':
      msg += ` → 到了股票市場！可以交易股票`;
      io.to(player.id).emit('stock_arrive', {});
      break;

    case 'bank_square':
      msg += ` → 到了銀行！可以存款或提款`;
      io.to(player.id).emit('bank_arrive', {});
      break;

    case 'jail':
      msg += ` → 探監（無影響）`;
      break;

    case 'free_parking':
      msg += ` → 免費停車，休息一下`;
      break;
  }

  addLog(msg);
  checkGameEnd();
}

function calcRent(sq, level) {
  return Math.floor(sq.rentBase * Math.pow(2, level));
}

function checkBankruptcy(player) {
  if (player.money < 0) {
    player.isBankrupt = true;
    player.money = 0;
    // 釋放地產
    Object.entries(game.properties).forEach(([pos, prop]) => {
      if (prop.ownerId === player.id) delete game.properties[pos];
    });
    addLog(`💀 ${player.name} 破產了！`);
    checkGameEnd();
  }
}

function checkGameEnd() {
  const alive = Object.values(game.players).filter(p => !p.isBankrupt);
  if (alive.length <= 1 && Object.keys(game.players).length > 1) {
    game.status = 'ended';
    const winner = alive[0];
    addLog(winner ? `🏆 ${winner.name} 獲勝！` : '所有玩家破產，平局！');
    io.emit('game_ended', { winner: winner ? winner.name : null });
  }
}

// ===== Socket.io 事件 =====
io.on('connection', (socket) => {
  console.log(`連線: ${socket.id}`);

  // 傳送目前狀態
  socket.emit('board_data', BOARD);
  socket.emit('game_state', buildClientState());

  // 加入遊戲
  socket.on('join', ({ name }) => {
    if (!name || name.trim().length === 0) return;
    if (game.status === 'ended') {
      game = createGame();
    }

    const color = PLAYER_COLORS[game.colorIndex % PLAYER_COLORS.length];
    game.colorIndex++;

    const player = {
      id: socket.id,
      name: name.trim().slice(0, 12),
      color,
      money: INITIAL_MONEY,
      position: 0,
      stamina: MAX_STAMINA,
      lastStaminaTime: Date.now(),
      bankDeposit: 0,
      bankDepositTime: Date.now(),
      stocks: {},
      jailTurns: 0,
      isBankrupt: false,
    };
    game.players[socket.id] = player;
    game.status = 'playing';

    addLog(`👤 ${player.name} 加入遊戲`);
    broadcastState();
  });

  // 擲骰子移動
  socket.on('roll_dice', () => {
    const player = game.players[socket.id];
    if (!player || player.isBankrupt) return;

    const stamina = calcStamina(player);
    if (stamina <= 0) {
      socket.emit('error_msg', '體力不足！請等待體力回復');
      return;
    }

    // 坐牢處理
    if (player.jailTurns > 0) {
      player.jailTurns--;
      addLog(`🔒 ${player.name} 在監獄服刑（剩餘 ${player.jailTurns} 回合）`);
      consumeStamina(player);
      broadcastState();
      return;
    }

    const dice1 = Math.ceil(Math.random() * 6);
    const dice2 = Math.ceil(Math.random() * 6);
    const steps = dice1 + dice2;

    consumeStamina(player);
    movePlayer(player, steps);
    addLog(`🎲 ${player.name} 擲出 ${dice1}+${dice2}=${steps}，移動到第 ${player.position} 格`);
    handleLanding(player);

    io.to(socket.id).emit('dice_result', { dice1, dice2, steps, position: player.position });
    broadcastState();
  });

  // 買地產
  socket.on('buy_property', ({ position }) => {
    const player = game.players[socket.id];
    if (!player || player.isBankrupt) return;

    const sq = BOARD[position];
    if (!sq || sq.type !== 'property') return;
    if (game.properties[position]) { socket.emit('error_msg', '此地產已被購買'); return; }
    if (player.money < sq.price) { socket.emit('error_msg', '金錢不足'); return; }

    player.money -= sq.price;
    game.properties[position] = { ownerId: socket.id, level: 0 };
    addLog(`🏘️ ${player.name} 購買「${sq.name}」-$${sq.price}`);
    broadcastState();
  });

  // 升級地產
  socket.on('upgrade_property', ({ position }) => {
    const player = game.players[socket.id];
    if (!player || player.isBankrupt) return;

    const sq = BOARD[position];
    const prop = game.properties[position];
    if (!prop || prop.ownerId !== socket.id) { socket.emit('error_msg', '不是你的地產'); return; }
    if (prop.level >= MAX_PROPERTY_LEVEL) { socket.emit('error_msg', '已達最高等級'); return; }

    const cost = sq.upgradeCost;
    if (player.money < cost) { socket.emit('error_msg', '金錢不足'); return; }

    player.money -= cost;
    prop.level++;
    const newRent = calcRent(sq, prop.level);
    addLog(`🏗️ ${player.name} 升級「${sq.name}」至 ${prop.level} 級，租金 $${newRent}`);
    broadcastState();
  });

  // 出售地產
  socket.on('sell_property', ({ position }) => {
    const player = game.players[socket.id];
    if (!player) return;

    const sq = BOARD[position];
    const prop = game.properties[position];
    if (!prop || prop.ownerId !== socket.id) { socket.emit('error_msg', '不是你的地產'); return; }

    const refund = Math.floor(sq.price * 0.7 + sq.upgradeCost * prop.level * 0.5);
    player.money += refund;
    delete game.properties[position];
    addLog(`💸 ${player.name} 出售「${sq.name}」+$${refund}`);
    broadcastState();
  });

  // 買股票
  socket.on('buy_stock', ({ stockId, amount }) => {
    const player = game.players[socket.id];
    const stock = game.stocks[stockId];
    if (!player || !stock || amount <= 0) return;

    const cost = stock.price * amount;
    if (player.money < cost) { socket.emit('error_msg', '金錢不足'); return; }

    player.money -= cost;
    player.stocks[stockId] = (player.stocks[stockId] || 0) + amount;
    addLog(`📈 ${player.name} 買入 ${stock.name} x${amount}（$${cost}）`);
    broadcastState();
  });

  // 賣股票
  socket.on('sell_stock', ({ stockId, amount }) => {
    const player = game.players[socket.id];
    const stock = game.stocks[stockId];
    if (!player || !stock || amount <= 0) return;

    const owned = player.stocks[stockId] || 0;
    if (owned < amount) { socket.emit('error_msg', '持股不足'); return; }

    const gain = stock.price * amount;
    player.money += gain;
    player.stocks[stockId] -= amount;
    if (player.stocks[stockId] === 0) delete player.stocks[stockId];
    addLog(`📉 ${player.name} 賣出 ${stock.name} x${amount}（+$${gain}）`);
    broadcastState();
  });

  // 打工
  socket.on('do_job', ({ jobId }) => {
    const player = game.players[socket.id];
    if (!player || player.isBankrupt) return;

    const job = game.jobs.find(j => j.id === jobId);
    if (!job) return;

    const lastDone = job.lastDone[socket.id] || 0;
    const now = Date.now();
    const remaining = job.cooldown - (now - lastDone);

    if (remaining > 0) {
      socket.emit('error_msg', `冷卻中，還需等 ${Math.ceil(remaining / 60000)} 分鐘`);
      return;
    }

    player.money += job.pay;
    job.lastDone[socket.id] = now;
    addLog(`💼 ${player.name} 完成「${job.name}」+$${job.pay}`);
    broadcastState();
  });

  // 銀行存款
  socket.on('bank_deposit', ({ amount }) => {
    const player = game.players[socket.id];
    if (!player) return;
    if (amount <= 0 || player.money < amount) { socket.emit('error_msg', '金額錯誤'); return; }

    // 結算現有利息
    const now = Date.now();
    const minutes = (now - player.bankDepositTime) / 60000;
    const interest = Math.floor(player.bankDeposit * 0.02 / 60 * minutes);
    player.bankDeposit += interest;
    player.bankDepositTime = now;

    player.money -= amount;
    player.bankDeposit += amount;
    addLog(`🏦 ${player.name} 存入銀行 $${amount}（利息已結算 +$${interest}）`);
    broadcastState();
  });

  // 銀行提款
  socket.on('bank_withdraw', ({ amount }) => {
    const player = game.players[socket.id];
    if (!player) return;

    // 結算現有利息
    const now = Date.now();
    const minutes = (now - player.bankDepositTime) / 60000;
    const interest = Math.floor(player.bankDeposit * 0.02 / 60 * minutes);
    player.bankDeposit += interest;
    player.bankDepositTime = now;

    const withdrawAmount = Math.min(amount, player.bankDeposit);
    if (withdrawAmount <= 0) { socket.emit('error_msg', '存款不足'); return; }

    player.money += withdrawAmount;
    player.bankDeposit -= withdrawAmount;
    addLog(`🏦 ${player.name} 提款 $${withdrawAmount}（利息 +$${interest}）`);
    broadcastState();
  });

  // 小遊戲：猜大小（高/低押注）
  socket.on('play_guess', ({ bet, guess }) => {
    const player = game.players[socket.id];
    if (!player || player.isBankrupt) return;
    if (bet <= 0 || player.money < bet) { socket.emit('error_msg', '押注金額錯誤'); return; }
    if (!['high', 'low', 'seven'].includes(guess)) return;

    const dice1 = Math.ceil(Math.random() * 6);
    const dice2 = Math.ceil(Math.random() * 6);
    const sum = dice1 + dice2;
    let result, win = false, multiplier = 1;

    if (sum > 7) result = 'high';
    else if (sum < 7) result = 'low';
    else result = 'seven';

    if (guess === result) {
      multiplier = guess === 'seven' ? 4 : 2;
      win = true;
    }

    if (win) {
      player.money += bet * (multiplier - 1);
      addLog(`🎰 ${player.name} 猜大小：${dice1}+${dice2}=${sum}，猜對！+$${bet * (multiplier - 1)}`);
    } else {
      player.money -= bet;
      addLog(`🎰 ${player.name} 猜大小：${dice1}+${dice2}=${sum}，猜錯 -$${bet}`);
      checkBankruptcy(player);
    }

    socket.emit('guess_result', { dice1, dice2, sum, guess, result, win, multiplier });
    broadcastState();
  });

  // 小遊戲：猜數字（1-10）
  socket.on('play_number', ({ bet, guess }) => {
    const player = game.players[socket.id];
    if (!player || player.isBankrupt) return;
    if (bet <= 0 || player.money < bet) { socket.emit('error_msg', '押注金額錯誤'); return; }

    const drawn = Math.ceil(Math.random() * 10);
    const win = drawn === guess;

    if (win) {
      player.money += bet * 8;
      addLog(`🎯 ${player.name} 猜數字：開出 ${drawn}，猜對！+$${bet * 8}`);
    } else {
      player.money -= bet;
      addLog(`🎯 ${player.name} 猜數字：開出 ${drawn}，猜錯 -$${bet}`);
      checkBankruptcy(player);
    }

    socket.emit('number_result', { drawn, guess, win });
    broadcastState();
  });

  // 繳交保釋金出獄
  socket.on('pay_bail', () => {
    const player = game.players[socket.id];
    if (!player || player.jailTurns === 0) return;
    const bail = 2000;
    if (player.money < bail) { socket.emit('error_msg', '金錢不足，無法繳交保釋金'); return; }
    player.money -= bail;
    player.jailTurns = 0;
    addLog(`🔓 ${player.name} 繳交保釋金 $${bail} 出獄`);
    broadcastState();
  });

  // 取得打工冷卻狀態
  socket.on('get_jobs', () => {
    const now = Date.now();
    const jobStatus = game.jobs.map(j => ({
      ...j,
      remaining: Math.max(0, j.cooldown - (now - (j.lastDone[socket.id] || 0))),
    }));
    socket.emit('jobs_data', jobStatus);
  });

  socket.on('disconnect', () => {
    console.log(`離線: ${socket.id}`);
    const player = game.players[socket.id];
    if (player) {
      addLog(`👋 ${player.name} 離線`);
      // 保留玩家資料（不刪除，玩家重連可繼續）
    }
  });
});

// ===== 定時器 =====
// 股票波動（每60秒）
setInterval(() => {
  if (game.status !== 'playing') return;
  Object.values(game.stocks).forEach(stock => {
    const change = (Math.random() * 2 - 1) * stock.volatility;
    stock.price = Math.max(10, Math.round(stock.price * (1 + change)));
  });
  io.emit('stock_update', game.stocks);
}, 60 * 1000);

// 體力推播（每30秒廣播當前體力狀態）
setInterval(() => {
  if (game.status !== 'playing') return;
  broadcastState();
}, 30 * 1000);

// 銀行利息（每5分鐘）
setInterval(() => {
  if (game.status !== 'playing') return;
  Object.values(game.players).forEach(player => {
    if (player.bankDeposit > 0) {
      const interest = Math.floor(player.bankDeposit * 0.02 / 12);
      if (interest > 0) {
        player.bankDeposit += interest;
        player.bankDepositTime = Date.now();
      }
    }
  });
}, 5 * 60 * 1000);

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`大富翁伺服器啟動：http://localhost:${PORT}`);
  console.log(`體力回復間隔：${STAMINA_REGEN_MS / 1000} 秒`);
});
