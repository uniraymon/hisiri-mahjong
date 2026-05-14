// 大富翁遊戲伺服器 - Node.js + Socket.io
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: { origin: '*', methods: ['GET', 'POST'] },
  transports: ['websocket', 'polling'],
  allowEIO3: true,
  pingTimeout: 60000,
  pingInterval: 25000,
});

app.use(express.static(path.join(__dirname, 'public')));

// ===== 常數 =====
const STAMINA_REGEN_MS = 5 * 60 * 1000; // 5分鐘回1體力（測試可改 30 * 1000）
const MAX_STAMINA = 5;
const INITIAL_MONEY = 15000;
const PASS_START_BONUS = 2000;
const BOARD_SIZE = 80;
const BOARD_COLS = 22; // 上下各22格
const BOARD_ROWS = 20; // 左右各20格（含角落）
const PLAYER_COLORS = ['#E74C3C','#3498DB','#2ECC71','#F39C12','#9B59B6','#E67E22'];
const MAX_PROPERTY_LEVEL = 4;

// ===== 地圖建置（80格，方形路徑圍繞台灣地圖）=====
// 格局：上22格(0-21) → 右18格(22-39) → 下22格(40-61) → 左18格(62-79)
// 角落：0=起點, 21=監獄, 40=自由廣場, 61=去坐牢
function buildBoard() {
  const _ = (type, name, opts = {}) => ({ type, name, color: '#BDC3C7', textColor: '#333', ...opts });
  const P = (name, grpName, color, price) => ({
    type: 'property', name,
    groupName: grpName, color, textColor: '#fff',
    price, rentBase: Math.floor(price * 0.1),
    upgradeCost: Math.floor(price * 0.5),
  });

  // 顏色常數
  const C = {
    PH:'#A0522D', KL:'#CD853F', TP:'#C0392B', NT:'#E74C3C',
    TY:'#8E44AD', YL:'#6C3483', HL:'#1A5276', TT:'#2471A3',
    PT:'#0E6655', KH:'#117A65', TN:'#1E8449', CY:'#196F3D',
    TC:'#1F618D', CH:'#2E4057', NI:'#4A235A', HC:'#784212',
  };

  const squares = [
    // ── 上排（位置 0-21，從左到右）────────────────────────────
    /*0 */ _('start',        '起　點',   { color:'#27AE60', textColor:'#fff', bonus: PASS_START_BONUS }),
    /*1 */ P('澎湖馬公', '澎湖群島', C.PH, 600),
    /*2 */ P('澎湖七美', '澎湖群島', C.PH, 650),
    /*3 */ _('chance',       '命　運',   { color:'#E67E22', textColor:'#fff' }),
    /*4 */ P('澎湖望安', '澎湖群島', C.PH, 700),
    /*5 */ P('基隆市',   '基　隆', C.KL, 800),
    /*6 */ _('airport',      '機　場',   { color:'#5DADE2', textColor:'#fff', fee: 500 }),
    /*7 */ P('基隆港',   '基　隆', C.KL, 900),
    /*8 */ P('基隆山',   '基　隆', C.KL, 1000),
    /*9 */ _('tax',          '稅務局',   { color:'#C0392B', textColor:'#fff', amount: 1000 }),
    /*10*/ P('台北松山', '台　北', C.TP, 1600),
    /*11*/ P('台北信義', '台　北', C.TP, 1800),
    /*12*/ _('chest',        '福　利',   { color:'#2980B9', textColor:'#fff' }),
    /*13*/ P('台北大安', '台　北', C.TP, 2000),
    /*14*/ P('台北中正', '台　北', C.TP, 2200),
    /*15*/ _('stock_market', '股票市場', { color:'#1ABC9C', textColor:'#fff' }),
    /*16*/ P('新北板橋', '新　北', C.NT, 1200),
    /*17*/ P('新北淡水', '新　北', C.NT, 1300),
    /*18*/ _('chance',       '命　運',   { color:'#E67E22', textColor:'#fff' }),
    /*19*/ P('新北九份', '新　北', C.NT, 1400),
    /*20*/ P('桃園大溪', '桃　園', C.TY, 1000),
    /*21*/ _('jail',         '監　獄',   { color:'#7F8C8D', textColor:'#fff' }),

    // ── 右排（位置 22-39，從上到下）─────────────────────────
    /*22*/ P('桃園市區', '桃　園', C.TY, 1100),
    /*23*/ P('桃園龜山', '桃　園', C.TY, 1200),
    /*24*/ _('tax',          '稅務局',   { color:'#C0392B', textColor:'#fff', amount: 1000 }),
    /*25*/ P('宜蘭市',   '宜　蘭', C.YL, 900),
    /*26*/ P('宜蘭礁溪', '宜　蘭', C.YL, 1000),
    /*27*/ _('chance',       '命　運',   { color:'#E67E22', textColor:'#fff' }),
    /*28*/ P('宜蘭冬山', '宜　蘭', C.YL, 1100),
    /*29*/ _('bank_square',  '銀　行',   { color:'#27AE60', textColor:'#fff' }),
    /*30*/ P('花蓮市',   '花　蓮', C.HL, 1100),
    /*31*/ P('花蓮太魯閣','花　蓮', C.HL, 1300),
    /*32*/ _('chest',        '福　利',   { color:'#2980B9', textColor:'#fff' }),
    /*33*/ P('花蓮七星潭','花　蓮', C.HL, 1400),
    /*34*/ _('hospital',     '醫　院',   { color:'#E91E63', textColor:'#fff', fee: 1500 }),
    /*35*/ P('台東市',   '台　東', C.TT, 900),
    /*36*/ P('台東知本', '台　東', C.TT, 1000),
    /*37*/ _('chance',       '命　運',   { color:'#E67E22', textColor:'#fff' }),
    /*38*/ P('台東池上', '台　東', C.TT, 1100),
    /*39*/ _('casino',       '賭　場',   { color:'#F39C12', textColor:'#fff' }),

    // ── 下排（位置 40-61，從右到左）─────────────────────────
    /*40*/ _('free_parking', '自由廣場', { color:'#8E44AD', textColor:'#fff' }),
    /*41*/ P('屏東恆春', '屏　東', C.PT, 900),
    /*42*/ P('屏東墾丁', '屏　東', C.PT, 1000),
    /*43*/ _('chance',       '命　運',   { color:'#E67E22', textColor:'#fff' }),
    /*44*/ P('屏東潮州', '屏　東', C.PT, 1100),
    /*45*/ P('高雄苓雅', '高　雄', C.KH, 1400),
    /*46*/ _('tax',          '稅務局',   { color:'#C0392B', textColor:'#fff', amount: 1200 }),
    /*47*/ P('高雄左營', '高　雄', C.KH, 1500),
    /*48*/ P('高雄鳳山', '高　雄', C.KH, 1600),
    /*49*/ P('高雄信義', '高　雄', C.KH, 1800),
    /*50*/ _('chest',        '福　利',   { color:'#2980B9', textColor:'#fff' }),
    /*51*/ P('台南安平', '台　南', C.TN, 1300),
    /*52*/ P('台南新化', '台　南', C.TN, 1400),
    /*53*/ _('chance',       '命　運',   { color:'#E67E22', textColor:'#fff' }),
    /*54*/ P('台南永康', '台　南', C.TN, 1500),
    /*55*/ P('台南仁德', '台　南', C.TN, 1600),
    /*56*/ _('bank_square',  '銀　行',   { color:'#27AE60', textColor:'#fff' }),
    /*57*/ P('嘉義市',   '嘉　義', C.CY, 1100),
    /*58*/ P('嘉義阿里山','嘉　義', C.CY, 1300),
    /*59*/ _('tax',          '稅務局',   { color:'#C0392B', textColor:'#fff', amount: 1000 }),
    /*60*/ P('嘉義朴子', '嘉　義', C.CY, 1000),
    /*61*/ _('go_to_jail',   '去坐牢',   { color:'#922B21', textColor:'#fff' }),

    // ── 左排（位置 62-79，從下到上）─────────────────────────
    /*62*/ P('台中市',   '台　中', C.TC, 1500),
    /*63*/ P('台中西屯', '台　中', C.TC, 1600),
    /*64*/ _('chance',       '命　運',   { color:'#E67E22', textColor:'#fff' }),
    /*65*/ P('台中北屯', '台　中', C.TC, 1700),
    /*66*/ P('台中太平', '台　中', C.TC, 1800),
    /*67*/ _('hospital',     '醫　院',   { color:'#E91E63', textColor:'#fff', fee: 1500 }),
    /*68*/ P('彰化市',   '彰　化', C.CH, 1000),
    /*69*/ P('彰化鹿港', '彰　化', C.CH, 1100),
    /*70*/ _('chest',        '福　利',   { color:'#2980B9', textColor:'#fff' }),
    /*71*/ P('彰化員林', '彰　化', C.CH, 1200),
    /*72*/ P('南投埔里', '南　投', C.NI, 900),
    /*73*/ _('chance',       '命　運',   { color:'#E67E22', textColor:'#fff' }),
    /*74*/ P('南投日月潭','南　投', C.NI, 1200),
    /*75*/ P('新竹市',   '新　竹', C.HC, 1100),
    /*76*/ P('新竹竹北', '新　竹', C.HC, 1200),
    /*77*/ _('tax',          '稅務局',   { color:'#C0392B', textColor:'#fff', amount: 1000 }),
    /*78*/ P('新竹內灣', '新　竹', C.HC, 1300),
    /*79*/ _('casino',       '賭　場',   { color:'#F39C12', textColor:'#fff' }),
  ];

  squares.forEach((s, i) => { s.position = i; });
  return squares;
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
