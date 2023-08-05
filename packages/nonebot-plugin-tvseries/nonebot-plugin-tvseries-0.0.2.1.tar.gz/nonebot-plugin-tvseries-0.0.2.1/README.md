# nonebot-plugin-tvseries

获取美剧

# 安装

## 环境(dockerfile)

```
ENV TZ=Asia/Shanghai
ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8
ENV TZ Asia/Shanghai
ENV DEBIAN_FRONTEND noninteractive
```

## 本体

`pip install nonebot-plugin-tvseries`

## 依赖

```
apt install -y libzbar0 locales locales-all fonts-noto
playwright install chromium && playwright install-deps
```

# 使用

`美剧` `tvseries`

# 有问题 提pr
有问题 提pr
