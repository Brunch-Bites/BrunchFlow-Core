import uvicorn
import logging
import sys
from pathlib import Path

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("BrunchFlow")

def start_server():
    """
    启动 BrunchFlow API 服务
    """
    logger.info("Initializing BrunchFlow Core Orchestrator...")
    
    # 注意：在生产环境中应通过环境变量控制配置
    uvicorn.run(
        "api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    start_server()
