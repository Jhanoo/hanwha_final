#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
plugin_checkout="$repo_root/.local/codex-plugins"
plugin_revision=5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f
command -v git >/dev/null || { echo 'Git이 필요합니다.' >&2; exit 1; }
if [[ ! -e "$plugin_checkout" ]]; then
  mkdir -p "$repo_root/.local"
  git clone --filter=blob:none --no-checkout https://github.com/openai/plugins.git "$plugin_checkout"
  git -C "$plugin_checkout" sparse-checkout init --cone
  git -C "$plugin_checkout" sparse-checkout set plugins/openai-developers plugins/plugin-eval
  git -C "$plugin_checkout" checkout --detach "$plugin_revision"
fi
if [[ "$(git -C "$plugin_checkout" rev-parse HEAD)" != "$plugin_revision" ]]; then
  echo '기존 플러그인 체크아웃의 버전이 다릅니다. 기존 변경을 확인한 뒤 별도로 갱신하세요.' >&2
  exit 1
fi
for plugin_name in openai-developers plugin-eval; do
  test -f "$plugin_checkout/plugins/$plugin_name/.codex-plugin/plugin.json"
done
if [[ "${1:-}" == '--prepare-only' ]]; then
  echo '플러그인 다운로드 및 프로젝트 marketplace 준비 완료'
  exit 0
fi
command -v codex >/dev/null || { echo 'Codex CLI를 설치한 뒤 이 스크립트를 다시 실행하세요.' >&2; exit 1; }
cd "$repo_root"
codex plugin marketplace add "$repo_root"
for plugin_name in openai-developers plugin-eval; do
  codex plugin add "$plugin_name@hanwha-it-agent"
done
codex plugin list --marketplace hanwha-it-agent
echo 'Codex를 재시작하세요.'
