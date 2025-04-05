"""
Configuration management for snooper-ai.
"""
import os
from pathlib import Path
from typing import Dict, Optional

import tomlkit

CONFIG_FILENAME = "pyproject.toml"

DEFAULT_CONFIG = {
    "tool": {
        "snooper-ai": {
            "provider": "claude",  # or "openai"
            "claude": {
                "model": "claude-3-7-sonnet-latest"
            },
            "openai": {
                "model": "gpt-4o"
            }
        }
    }
}

def find_project_root(start_path: Path = None) -> Optional[Path]:
    """Find the project root by looking for pyproject.toml."""
    if start_path is None:
        start_path = Path.cwd()
    
    current = start_path
    while current != current.parent:
        if (current / CONFIG_FILENAME).exists():
            return current
        current = current.parent
    return None

def load_config() -> Dict:
    """Load configuration from pyproject.toml."""
    root = find_project_root()
    if not root:
        return DEFAULT_CONFIG["tool"]["snooper-ai"]
    
    config_path = root / CONFIG_FILENAME
    if not config_path.exists():
        return DEFAULT_CONFIG["tool"]["snooper-ai"]
    
    try:
        with open(config_path, "r") as f:
            config = tomlkit.parse(f.read())
        return config.get("tool", {}).get("snooper-ai", DEFAULT_CONFIG["tool"]["snooper-ai"])
    except Exception:
        return DEFAULT_CONFIG["tool"]["snooper-ai"]

def save_config(config: Dict) -> None:
    """Save configuration to pyproject.toml."""
    root = find_project_root()
    if not root:
        root = Path.cwd()
    
    config_path = root / CONFIG_FILENAME
    
    try:
        if config_path.exists():
            with open(config_path, "r") as f:
                full_config = tomlkit.parse(f.read())
        else:
            full_config = tomlkit.document()
        
        if "tool" not in full_config:
            full_config["tool"] = {}
        
        full_config["tool"]["snooper-ai"] = config
        
        with open(config_path, "w") as f:
            f.write(tomlkit.dumps(full_config))
    except Exception as e:
        raise ValueError(f"Failed to save configuration: {e}")

def setup_initial_config(console) -> Dict:
    """Interactive configuration setup."""
    from rich.prompt import Prompt, Confirm
    
    config = DEFAULT_CONFIG["tool"]["snooper-ai"].copy()
    
    console.print("\n[info]Let's set up your snooper-ai configuration.[/info]")
    
    # Choose default provider
    provider = Prompt.ask(
        "\n[info]Which AI provider would you like to use?[/info]",
        choices=["claude", "openai"],
        default="claude"
    )
    config["provider"] = provider
    
    # Configure Claude
    if provider == "claude" or Confirm.ask("\n[info]Would you like to configure Claude as a backup?[/info]"):
        config["claude"]["model"] = "claude-3-7-sonnet-latest"  # Using latest model
        
        if not os.getenv("ANTHROPIC_API_KEY"):
            api_key = Prompt.ask(
                "\n[info]Please enter your Anthropic API key (or set ANTHROPIC_API_KEY env var later)[/info]",
                password=True,
                default=""
            )
            if api_key:
                os.environ["ANTHROPIC_API_KEY"] = api_key
    
    # Configure OpenAI
    if provider == "openai" or Confirm.ask("\n[info]Would you like to configure OpenAI as a backup?[/info]"):
        config["openai"]["model"] = "gpt-4o"  # Using latest model
        
        if not os.getenv("OPENAI_API_KEY"):
            api_key = Prompt.ask(
                "\n[info]Please enter your OpenAI API key (or set OPENAI_API_KEY env var later)[/info]",
                password=True,
                default=""
            )
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
    
    # Save the configuration
    try:
        save_config(config)
        console.print("\n[success]Configuration saved successfully![/success]")
    except Exception as e:
        console.print(f"\n[warning]Failed to save configuration: {e}[/warning]")
        console.print("[warning]Will use the configuration for this session only.[/warning]")
    
    return config 