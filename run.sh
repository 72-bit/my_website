#!/bin/bash

if ! command -v tmux &> /dev/null; then
    echo "tmux chưa được cài đặt. Đang cài đặt..."
    sudo apt update && sudo apt install tmux -y
fi

# Tạo session và các lệnh như cũ
tmux new-session -d -s web-tunnel
tmux send-keys -t web-tunnel "python3 app.py" C-m
tmux split-window -v -t web-tunnel
tmux send-keys -t web-tunnel "sleep 3 && sudo cloudflared tunnel --config /etc/cloudflared/config.yml run pi-tunnel" C-m

# Đính kèm session
tmux attach-session -t web-tunnel

# SAU KHI THOÁT KHỎI TMUX: Tự động xóa toàn bộ session và các tiến trình bên trong
tmux kill-session -t web-tunnel 2>/dev/null
