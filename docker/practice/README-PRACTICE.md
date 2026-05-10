# Docker Compose 多服务实践

## 项目结构

```
docker/
├── docker-compose.yml      # Compose 配置文件（2 个服务）
├── html/
│   └── index.html          # Nginx 网页（带 API 测试）
└── api/
    ├── Dockerfile          # Flask 镜像构建文件
    ├── app.py              # Flask 应用代码
    └── requirements.txt    # Python 依赖
```

## 服务说明

### 1. Web 服务 (Nginx)
- **镜像**: nginx:alpine
- **端口**: 8080 → 80
- **功能**: 提供静态网页
- **依赖**: api 服务

### 2. API 服务 (Flask)
- **构建**: 自定义镜像
- **端口**: 5000 → 5000
- **功能**: 提供 REST API
- **环境**: FLASK_ENV=development

## 快速开始

### 1. 启动所有服务
```bash
docker-compose up -d
```

### 2. 查看服务状态
```bash
docker-compose ps
```

**预期输出**：
```
NAME              STATUS         PORTS
docker-api-1      Up             0.0.0.0:5000->5000/tcp
docker-web-1      Up             0.0.0.0:8080->80/tcp
```

### 3. 访问网页
打开浏览器访问：http://localhost:8080

### 4. 测试 API
- **方法 1**: 点击网页上的"测试 API 服务"按钮
- **方法 2**: 直接访问 http://localhost:5000/
- **方法 3**: 访问健康检查 http://localhost:5000/health

### 5. 查看日志
```bash
# 查看所有服务日志
docker-compose logs -f

# 只查看 API 服务日志
docker-compose logs -f api

# 只查看 Web 服务日志
docker-compose logs -f web
```

### 6. 进入容器
```bash
# 进入 API 容器
docker-compose exec api sh

# 进入 Web 容器
docker-compose exec web sh
```

### 7. 停止服务
```bash
docker-compose stop
```

### 8. 删除服务
```bash
docker-compose down
```

## 实践任务

### 任务 1：观察服务启动顺序
```bash
docker-compose up -d
```
观察输出，看看哪个服务先启动？为什么？

**答案**：api 服务先启动，因为 web 服务配置了 `depends_on: - api`

### 任务 2：修改 API 代码
1. 编辑 `api/app.py`，添加新的路由
2. 重新构建并启动：
```bash
docker-compose up -d --build api
```
3. 测试新功能

### 任务 3：添加新服务
在 `docker-compose.yml` 中添加 Redis 服务：
```yaml
redis:
  image: redis:alpine
  ports:
    - "6379:6379"
```

然后启动：
```bash
docker-compose up -d
```

## Docker Compose 优势体验

### 对比：使用 docker run

```bash
# 启动 API 服务
docker build -t my-flask-api ./api
docker run -d -p 5000:5000 --name api -e FLASK_ENV=development my-flask-api

# 启动 Web 服务
docker run -d -p 8080:80 --name web \
  -v $(pwd)/html:/usr/share/nginx/html \
  --link api \
  nginx:alpine
```

### 使用 docker-compose

```bash
docker-compose up -d
```

**优势**：
- ✅ 一个命令启动所有服务
- ✅ 配置文件即文档
- ✅ 自动处理依赖关系
- ✅ 统一管理环境变量
- ✅ 轻松扩展服务

## 常用命令速查

| 命令 | 说明 |
|------|------|
| `docker-compose up -d` | 启动所有服务 |
| `docker-compose up -d --build` | 重新构建并启动 |
| `docker-compose ps` | 查看服务状态 |
| `docker-compose logs -f` | 查看日志 |
| `docker-compose stop` | 停止服务 |
| `docker-compose down` | 删除服务 |
| `docker-compose exec <service> sh` | 进入容器 |
| `docker-compose restart` | 重启服务 |

## 故障排查

### 问题 1：API 服务启动失败
```bash
# 查看日志
docker-compose logs api

# 重新构建
docker-compose build api
```

### 问题 2：端口冲突
如果 5000 或 8080 端口被占用，修改 `docker-compose.yml`：
```yaml
ports:
  - "5001:5000"  # 改用 5001 端口
```

### 问题 3：服务无法通信
检查服务名是否正确，容器间使用服务名通信：
```python
# 在 web 服务中访问 api
http://api:5000/
```

## 总结

通过这个实践，你学会了：
- ✅ 配置多服务 Docker Compose
- ✅ 服务依赖管理（depends_on）
- ✅ 自定义镜像构建
- ✅ 环境变量配置
- ✅ 服务间通信
- ✅ 日志查看和故障排查

继续探索，尝试添加数据库服务吧！
