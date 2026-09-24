(() => {
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  document.querySelectorAll(".code").forEach((block) => {
    const button = block.querySelector(".copy");
    const code = block.querySelector("code");
    if (!button || !code) {
      return;
    }
    button.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(code.innerText.replace(/\n$/, ""));
        button.textContent = "Copied";
      } catch (error) {
        button.textContent = "Press Ctrl+C";
        const range = document.createRange();
        range.selectNodeContents(code);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
      }
      setTimeout(() => {
        button.textContent = "Copy";
      }, 1600);
    });
  });

  const tocLinks = [...document.querySelectorAll(".toc a")];
  if (tocLinks.length && "IntersectionObserver" in window) {
    const byId = new Map(tocLinks.map((link) => [link.getAttribute("href").slice(1), link]));
    const visible = new Set();
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          visible.add(entry.target.id);
        } else {
          visible.delete(entry.target.id);
        }
      });
      const first = [...byId.keys()].find((id) => visible.has(id));
      tocLinks.forEach((link) => link.classList.toggle("on", byId.get(first) === link));
    }, { rootMargin: "-80px 0px -55% 0px" });
    byId.forEach((link, id) => {
      const section = document.getElementById(id);
      if (section) {
        observer.observe(section);
      }
    });
  }

  if (window.hljs) {
    document.querySelectorAll("pre code[class*='language-']").forEach((node) => window.hljs.highlightElement(node));
  }

  const canvas = document.getElementById("regions");
  if (!canvas) {
    return;
  }
  const context = canvas.getContext("2d");
  const figure = canvas.closest("figure");
  const statThreads = figure.querySelector("[data-stat='threads']");
  const statHandoffs = figure.querySelector("[data-stat='handoffs']");
  const statTick = figure.querySelector("[data-stat='tick']");
  const palette = ["--lapis", "--emerald", "--copper", "--amethyst", "--redstone", "--gold", "--prismarine"];

  let seed = 20260923;
  const random = () => {
    seed = (seed * 1664525 + 1013904223) >>> 0;
    return seed / 4294967296;
  };

  const COLS = 32;
  const ROWS = 20;
  const regions = palette.map((token, index) => ({
    token,
    x: 3 + random() * (COLS - 6),
    y: 2 + random() * (ROWS - 4),
    period: 900 + index * 173 + random() * 500,
    phase: random() * 1000,
    ticks: 0,
    color: "#888"
  }));

  const owner = [];
  for (let row = 0; row < ROWS; row++) {
    for (let col = 0; col < COLS; col++) {
      let best = 0;
      let bestDistance = Infinity;
      regions.forEach((region, index) => {
        const wobble = Math.sin(col * 0.9 + index) * 0.8 + Math.cos(row * 1.3 - index) * 0.8;
        const distance = Math.hypot(col - region.x, (row - region.y) * 1.15) + wobble;
        if (distance < bestDistance) {
          bestDistance = distance;
          best = index;
        }
      });
      owner.push(best);
    }
  }
  const regionAt = (col, row) => owner[Math.max(0, Math.min(ROWS - 1, row)) * COLS + Math.max(0, Math.min(COLS - 1, col))];

  const players = Array.from({ length: 16 }, () => {
    const col = Math.floor(random() * COLS);
    const row = Math.floor(random() * ROWS);
    return { col, row, fromCol: col, fromRow: row, start: 0, duration: 600, region: regionAt(col, row), flash: 0 };
  });

  let handoffs = 0;
  const flashes = [];

  const readColors = () => {
    const style = getComputedStyle(canvas);
    regions.forEach((region) => {
      region.color = style.getPropertyValue(region.token).trim() || "#888";
    });
    return {
      ground: style.getPropertyValue("--deep-ground").trim() || "#101114",
      grid: style.getPropertyValue("--deep-line").trim() || "#23262d",
      player: "#f4f1ea"
    };
  };
  let colors = readColors();
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
    colors = readColors();
  });

  let width = 0;
  let height = 0;
  let tile = 0;
  const resize = () => {
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    const box = canvas.getBoundingClientRect();
    width = box.width;
    height = box.height;
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    tile = Math.min(width / COLS, height / ROWS);
  };

  const hexToRgb = (hex) => {
    const value = hex.replace("#", "");
    const full = value.length === 3 ? value.split("").map((c) => c + c).join("") : value;
    const number = parseInt(full, 16);
    return [(number >> 16) & 255, (number >> 8) & 255, number & 255];
  };

  const step = (player, now) => {
    const options = [[1, 0], [-1, 0], [0, 1], [0, -1]];
    const [dx, dy] = options[Math.floor(random() * options.length)];
    player.fromCol = player.col;
    player.fromRow = player.row;
    player.col = Math.max(0, Math.min(COLS - 1, player.col + dx));
    player.row = Math.max(0, Math.min(ROWS - 1, player.row + dy));
    player.start = now;
    player.duration = 380 + random() * 520;
    const next = regionAt(player.col, player.row);
    if (next !== player.region) {
      player.region = next;
      handoffs++;
      flashes.push({ col: player.col, row: player.row, born: now, color: regions[next].color });
    }
  };

  const draw = (now) => {
    context.fillStyle = colors.ground;
    context.fillRect(0, 0, width, height);
    const offsetX = (width - tile * COLS) / 2;
    const offsetY = (height - tile * ROWS) / 2;

    regions.forEach((region) => {
      const t = ((now + region.phase) % region.period) / region.period;
      region.wave = t;
      region.ticks = Math.floor((now + region.phase) / region.period);
    });

    for (let row = 0; row < ROWS; row++) {
      for (let col = 0; col < COLS; col++) {
        const index = regionAt(col, row);
        const region = regions[index];
        const distance = Math.hypot(col - region.x, row - region.y) / 12;
        const ring = Math.max(0, 1 - Math.abs(region.wave - distance) * 7);
        const [r, g, b] = hexToRgb(region.color);
        const alpha = 0.13 + ring * 0.42;
        context.fillStyle = `rgba(${r},${g},${b},${alpha})`;
        const x = offsetX + col * tile;
        const y = offsetY + row * tile;
        context.fillRect(x + 1, y + 1, tile - 2, tile - 2);
        const right = col + 1 < COLS && regionAt(col + 1, row) !== index;
        const below = row + 1 < ROWS && regionAt(col, row + 1) !== index;
        if (right || below) {
          context.fillStyle = `rgba(${r},${g},${b},0.9)`;
          if (right) {
            context.fillRect(x + tile - 1.5, y, 1.5, tile);
          }
          if (below) {
            context.fillRect(x, y + tile - 1.5, tile, 1.5);
          }
        }
      }
    }

    for (let index = flashes.length - 1; index >= 0; index--) {
      const flash = flashes[index];
      const age = (now - flash.born) / 700;
      if (age >= 1) {
        flashes.splice(index, 1);
        continue;
      }
      const [r, g, b] = hexToRgb(flash.color);
      context.strokeStyle = `rgba(${r},${g},${b},${1 - age})`;
      context.lineWidth = 2;
      const grow = age * tile * 0.9;
      context.strokeRect(offsetX + flash.col * tile - grow, offsetY + flash.row * tile - grow, tile + grow * 2, tile + grow * 2);
    }

    players.forEach((player) => {
      if (now - player.start >= player.duration) {
        step(player, now);
      }
      const k = Math.min(1, (now - player.start) / player.duration);
      const ease = k * k * (3 - 2 * k);
      const col = player.fromCol + (player.col - player.fromCol) * ease;
      const row = player.fromRow + (player.row - player.fromRow) * ease;
      const size = Math.max(4, tile * 0.38);
      context.fillStyle = colors.player;
      context.fillRect(offsetX + col * tile + (tile - size) / 2, offsetY + row * tile + (tile - size) / 2, size, size);
    });

    if (statThreads) {
      statThreads.textContent = String(regions.length);
      statHandoffs.textContent = String(handoffs);
      statTick.textContent = String(regions.reduce((sum, region) => sum + region.ticks, 0));
    }
  };

  resize();
  window.addEventListener("resize", () => {
    resize();
    draw(performance.now());
  });

  if (reduced) {
    draw(1800);
    return;
  }

  let running = false;
  const loop = (now) => {
    if (!running) {
      return;
    }
    draw(now);
    requestAnimationFrame(loop);
  };
  const start = () => {
    if (!running) {
      running = true;
      requestAnimationFrame(loop);
    }
  };
  draw(performance.now());
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting && !document.hidden) {
        start();
      } else {
        running = false;
      }
    }).observe(canvas);
  } else {
    start();
  }
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      running = false;
    } else {
      start();
    }
  });
})();
