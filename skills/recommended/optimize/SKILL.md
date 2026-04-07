---
name: optimize
description: 提升界面性能，包括加载速度、渲染、动画、图片和包体积。让体验更快更流畅。Improve interface performance across loading speed, rendering, animations, images, and bundle size.
user-invokable: true
argument-hint: [TARGET=<value>]
---

识别并修复性能问题，创造更快、更流畅的用户体验。

## 评估性能问题

了解当前性能并识别问题：

1. **测量当前状态**：
   - **Core Web Vitals**：LCP、FID/INP、CLS 分数
   - **加载时间**：可交互时间、首次内容绘制
   - **包体积**：JavaScript、CSS、图片大小
   - **运行时性能**：帧率、内存使用、CPU 使用
   - **网络**：请求数、payload 大小、瀑布流

2. **识别瓶颈**：
   - 什么慢？（初始加载？交互？动画？）
   - 什么导致的？（大图片？昂贵的 JavaScript？布局抖动？）
   - 有多严重？（可感知？烦人？阻塞？）
   - 影响谁？（所有用户？只有移动端？慢速连接？）

**关键**：测量前和后。提前优化浪费时间。只优化真正重要的。

## 优化策略

创建系统性改进计划：

### 加载性能

**优化图片**：
- 使用现代格式（WebP、AVIF）
- 正确尺寸（不要为 300px 显示加载 3000px 图片）
- 懒加载折叠下方图片
- 响应式图片（`srcset`、`picture` 元素）
- 压缩图片（80-85% 质量通常难以察觉）
- 使用 CDN 加快交付

```html
<img 
  src="hero.webp"
  srcset="hero-400.webp 400w, hero-800.webp 800w, hero-1200.webp 1200w"
  sizes="(max-width: 400px) 400px, (max-width: 800px) 800px, 1200px"
  loading="lazy"
  alt="Hero image"
/>
```

**减少 JavaScript 包**：
- 代码分割（按路由、按组件）
- Tree shaking（移除未使用代码）
- 移除未使用依赖
- 懒加载非关键代码
- 对大组件使用动态导入

```javascript
// 懒加载重型组件
const HeavyChart = lazy(() => import('./HeavyChart'));
```

**优化 CSS**：
- 移除未使用 CSS
- 关键 CSS 内联，其余异步
- 最小化 CSS 文件
- 使用 CSS containment 隔离独立区域

**优化字体**：
- 使用 `font-display: swap` 或 `optional`
- 子集化字体（只加载需要的字符）
- 预加载关键字体
- 适当使用系统字体
- 限制加载的字体重量

```css
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap; /* 立即显示后备 */
  unicode-range: U+0020-007F; /* 仅基本拉丁字母 */
}
```

**优化加载策略**：
- 关键资源优先（非关键异步/defer）
- 预加载关键资源
- 预取可能的下一页
- Service worker 离线/缓存
- HTTP/2 或 HTTP/3 多路复用

### 渲染性能

**避免布局抖动**：
```javascript
// ❌ 差：交替读写（导致回流）
elements.forEach(el => {
  const height = el.offsetHeight; // 读（强制布局）
  el.style.height = height * 2; // 写
});

// ✅ 好：批量读，然后批量写
const heights = elements.map(el => el.offsetHeight); // 全部读
elements.forEach((el, i) => {
  el.style.height = heights[i] * 2; // 全部写
});
```

**优化渲染**：
- 对独立区域使用 CSS `contain` 属性
- 最小化 DOM 深度（扁平更快）
- 减少 DOM 数量（元素越少越好）
- 对长列表使用 `content-visibility: auto`
- 对超长列表使用虚拟滚动（react-window、react-virtualized）

**减少绘制与合成**：
- 使用 `transform` 和 `opacity` 做动画（GPU 加速）
- 避免动画布局属性（width、height、top、left）
- 谨慎使用 `will-change` 处理已知昂贵操作
- 最小化绘制区域（越小越快）

### 动画性能

**GPU 加速**：
```css
/* ✅ GPU 加速（快） */
.animated {
  transform: translateX(100px);
  opacity: 0.5;
}

/* ❌ CPU 绑定（慢） */
.animated {
  left: 100px;
  width: 300px;
}
```

**流畅 60fps**：
- 目标每帧 16ms（60fps）
- 对 JS 动画使用 `requestAnimationFrame`
- 对滚动处理函数去抖/节流
- 尽可能使用 CSS 动画
- 动画期间避免长时间运行的 JavaScript

**Intersection Observer**：
```javascript
// 高效检测元素何时进入视口
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      // 元素可见，懒加载或动画
    }
  });
});
```

### React/框架优化

**React 特定**：
- 对昂贵组件使用 `memo()`
- 对昂贵计算使用 `useMemo()` 和 `useCallback()`
- 虚拟化长列表
- 路由代码分割
- 避免在渲染中创建内联函数
- 使用 React DevTools Profiler

**框架通用**：
- 最小化重渲染
- 对昂贵操作去抖
- 记忆化计算值
- 懒加载路由和组件

### 网络优化

**减少请求**：
- 合并小文件
- 对图标使用 SVG sprites
- 内联小型关键资源
- 移除未使用的第三方脚本

**优化 API**：
- 使用分页（不要加载所有内容）
- GraphQL 只请求需要的字段
- 响应压缩（gzip、brotli）
- HTTP 缓存头
- CDN 提供静态资源

**针对慢速连接优化**：
- 基于连接的自适应加载（navigator.connection）
- 乐观 UI 更新
- 请求优先级
- 渐进增强

## Core Web Vitals 优化

### 最大内容绘制（LCP < 2.5s）
- 优化 Hero 图片
- 内联关键 CSS
- 预加载关键资源
- 使用 CDN
- 服务端渲染

### 首次输入延迟（FID < 100ms）/ INP（< 200ms）
- 拆分长任务
- 延迟非关键 JavaScript
- 对重型计算使用 Web Workers
- 减少 JavaScript 执行时间

### 累积布局偏移（CLS < 0.1）
- 为图片和视频设置尺寸
- 不要在现有内容上方注入内容
- 使用 CSS `aspect-ratio` 属性
- 为广告/嵌入预留空间
- 避免导致布局偏移的动画

```css
/* 为图片预留空间 */
.image-container {
  aspect-ratio: 16 / 9;
}
```

## 性能监控

**使用的工具**：
- Chrome DevTools（Lighthouse、Performance 面板）
- WebPageTest
- Core Web Vitals（Chrome UX 报告）
- 包分析器（webpack-bundle-analyzer）
- 性能监控（Sentry、DataDog、New Relic）

**关键指标**：
- LCP、FID/INP、CLS（Core Web Vitals）
- Time to Interactive（TTI）
- First Contentful Paint（FCP）
- Total Blocking Time（TBT）
- 包大小
- 请求数

**最重要**：在真实设备和真实网络条件下测量。桌面 Chrome 加快速连接不代表实际情况。

**禁止**：
- 不测量就优化（提前优化）
- 为性能牺牲无障碍
- 优化时破坏功能
- 到处使用 `will-change`（创建新层，消耗内存）
- 懒加载折叠上方内容
- 忽略主要问题而优化微优化（先优化最大瓶颈）
- 忘记移动端性能（通常是更慢的设备和更慢的连接）

## 验证改进

测试优化是否有效：

- **前/后指标**：比较 Lighthouse 分数
- **真实用户监控**：跟踪真实用户的改进
- **不同设备**：在低端 Android 上测试，不只是旗舰 iPhone
- **慢速连接**：节流到 3G，测试体验
- **无回归**：确保功能仍然正常
- **用户感知**：它*感觉*更快了吗？

记住：性能是一个特性。快速体验感觉更响应、更精致、更专业。系统化优化，严格测量，优先考虑用户可感知的性能。
