"""
Command-line interface for snooper-ai.
"""
import io
import os
import sys
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.syntax import Syntax
from rich.theme import Theme

from .config import load_config, setup_initial_config
from .llm.claude import ClaudeProvider
from .llm.openai import OpenAIProvider

# Create a custom theme for our CLI
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red bold",
    "success": "green",
})

console = Console(theme=custom_theme)

def display_trace(trace_output: str):
    """Display the trace output."""
    print(trace_output)

def get_llm_provider(config: dict, api_key: Optional[str] = None):
    """Get the appropriate LLM provider based on configuration."""
    provider = config["provider"]
    
    try:
        if provider == "claude":
            return ClaudeProvider(
                api_key=api_key,
                model=config["claude"]["model"]
            ), provider
        elif provider == "openai":
            return OpenAIProvider(
                api_key=api_key,
                model=config["openai"]["model"]
            ), provider
    except ValueError as e:
        # If primary provider fails, try the backup
        console.print(f"\n[warning]Failed to initialize {provider}: {e}[/warning]")
        console.print("[info]Trying backup provider...[/info]")
        
        backup_provider = "openai" if provider == "claude" else "claude"
        try:
            if backup_provider == "claude":
                return ClaudeProvider(model=config["claude"]["model"]), backup_provider
            else:
                return OpenAIProvider(model=config["openai"]["model"]), backup_provider
        except ValueError as e:
            raise ValueError(f"Failed to initialize both providers: {e}")
    
    raise ValueError(f"Unknown provider: {provider}")

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """snooper-ai - Debug your Python code with AI assistance.

    Available commands:
        run     Run a Python file with AI-enhanced debugging
                Example: snooper run script.py --show-trace
        
        config  Configure snooper-ai settings
                Example: snooper config
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

@cli.command(name="run")
@click.argument('file', type=click.Path(exists=True, dir_okay=False))
@click.option('--api-key', help='API key for the selected provider')
@click.option('--show-trace/--no-show-trace', default=False,
              help='Show the detailed execution trace including variable changes and line execution (default: False)')
def run_file(file: str, api_key: str, show_trace: bool):
    """Run a Python file with AI-enhanced debugging.
    
    FILE is the Python file to analyze. The file should use @snoop() decorator
    to enable tracing of the code execution.
    
    Examples:
        snooper run my_script.py
        snooper run my_script.py --show-trace
        snooper run my_script.py --api-key your-api-key
    """
    try:
        # Show a welcome message
        console.print(Panel.fit(
            "[success]🔍 snooper-ai[/success] - Debug your Python code with AI",
            subtitle="",
            width=100,
            padding=(0, 2)
        ))
        
        # Load configuration
        config = load_config()
        if not config:
            config = setup_initial_config(console)
        
        # Get user's question
        user_query = Prompt.ask("\n[info]What would you like to know about the code execution?")
        
        # Show progress
        with console.status("[info]Running your code and capturing execution trace..."):
            # Capture all output in a single buffer
            output_buffer = io.StringIO()
            
            try:
                with redirect_stdout(output_buffer), redirect_stderr(output_buffer):
                    # Get the file's directory to properly handle imports
                    file_dir = str(Path(file).parent)
                    if file_dir not in sys.path:
                        sys.path.insert(0, file_dir)
                    
                    # Execute the Python file as a module
                    import importlib.util
                    spec = importlib.util.spec_from_file_location("module", file)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
            except Exception as e:
                # Capture the error and traceback
                import traceback
                error_trace = traceback.format_exc()
                output_buffer.write("\n\nError occurred:\n" + error_trace)
                console.print(f"\n[error]Error occurred during execution:[/error]")
                console.print(Panel(error_trace, title="Error Details", style="red"))
            
            trace_output = output_buffer.getvalue()
            if show_trace:
                print(f"{trace_output}")
        
        # Initialize LLM provider
        provider, actual_provider = get_llm_provider(config, api_key)
        
        with console.status(f"[info]Getting AI analysis using {actual_provider.title()}..."):
            analysis = provider.analyze_trace(trace_output, user_query)
        
        # Display the analysis
        console.print(f"\n[success]Analysis from {actual_provider.title()}:[/success]")
        console.print(Panel(analysis, expand=False))
        
    except ValueError as e:
        console.print(f"\n[error]Error:[/error] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[error]Error:[/error] An unexpected error occurred: {e}")
        sys.exit(1)

@cli.command(name="config")
def configure():
    """Configure snooper-ai settings."""
    try:
        console.print(Panel.fit(
            "[success]🔧 snooper-ai[/success] - Configure your snooper-ai settings",
            width=100,
            padding=(0, 2)
        ))
        
        config = setup_initial_config(console)
        
        # Show current configuration
        console.print("\n[info]Current configuration:[/info]")
        console.print(Panel(~
            f"Provider: [success]{config['provider']}[/success]\n"
            f"Claude Model: [success]{config['claude']['model']}[/success]\n"
            f"OpenAI Model: [success]{config['openai']['model']}[/success]",
            title="[info]Settings[/info]"
        ))
        
    except Exception as e:
        console.print(f"\n[error]Error:[/error] An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    cli() 