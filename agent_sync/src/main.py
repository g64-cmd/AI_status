"""
The CLI Entry point for the Project Status Log tool.
"""
import argparse
import json
import sys
from . import storage, manager, models

# The default path to the JSON database file.
DEFAULT_DB_PATH = "./status_log.json"


def parse_arguments() -> argparse.Namespace:
    """
    Defines and parses CLI arguments for subcommands: add, read, complete.

    Returns:
        The parsed arguments as a namespace object.
    """
    parser = argparse.ArgumentParser(
        description="AI Project Status Log Tool - Manage tasks across AI agents"
    )
    
    # Global flag for JSON output
    # This is crucial for Agent integration, allowing them to parse the output reliably.
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON for agent parsing'
    )
    
    # Create subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # 'add' command
    add_parser = subparsers.add_parser('add', help='Add a new log entry')
    add_parser.add_argument('--desc', required=True, help='Description of the task')
    add_parser.add_argument('--priority', required=True, 
                           choices=['tier0', 'tier1', 'tier2', 'tier3'],
                           help='Priority tier (tier0=critical, tier3=weak)')
    add_parser.add_argument('--user', required=True, help='Creator name')
    add_parser.add_argument('--role', required=True,
                           choices=['planner', 'engineer', 'user'],
                           help='Creator role')
    
    # 'read' command
    read_parser = subparsers.add_parser('read', help='Read and display all log entries (sorted)')
    
    # 'complete' command
    complete_parser = subparsers.add_parser('complete', help='Mark a log entry as completed')
    complete_parser.add_argument('--id', required=True, help='ID of the entry to complete')
    complete_parser.add_argument('--user', required=True, help='Completer name')
    complete_parser.add_argument('--role', required=True,
                                choices=['planner', 'engineer', 'user'],
                                help='Completer role')
    
    return parser.parse_args()


def main() -> None:
    """
    The main function. Parses arguments and dispatches to the appropriate
    business logic based on the provided subcommand.
    """
    args = parse_arguments()
    
    if not args.command:
        print("Error: No command specified. Use -h for help.", file=sys.stderr)
        sys.exit(1)
    
    try:
        if args.command == 'add':
            # Create the new entry object first to validate inputs
            new_entry = manager.create_entry(
                description=args.desc,
                priority=args.priority,
                creator=args.user,
                role=args.role
            )
            
            # More efficient add: load dicts, append a new dict, save dicts
            log_dicts = storage.load_logs(DEFAULT_DB_PATH)
            log_dicts.append(models.to_dict(new_entry))
            storage.save_logs(DEFAULT_DB_PATH, log_dicts)
            
            # Output result
            if args.json:
                result = {
                    "status": "success",
                    "data": models.to_dict(new_entry)
                }
                json.dump(result, sys.stdout, indent=2)
            else:
                print(f"✓ Created entry: {new_entry.id}")
                print(f"  Description: {new_entry.description}")
                print(f"  Priority: {new_entry.priority}")
                print(f"  Status: {new_entry.status}")
        
        elif args.command == 'read':
            # Load and sort logs
            log_dicts = storage.load_logs(DEFAULT_DB_PATH)
            logs = [models.from_dict(d) for d in log_dicts]
            sorted_logs = manager.sort_logs(logs)
            
            # Output result
            if args.json:
                result = [models.to_dict(entry) for entry in sorted_logs]
                json.dump(result, sys.stdout, indent=2)
            else:
                if not sorted_logs:
                    print("No log entries found.")
                else:
                    print(f"\n{'='*80}")
                    print(f"PROJECT STATUS LOG ({len(sorted_logs)} entries)")
                    print(f"{'='*80}\n")
                    
                    for i, entry in enumerate(sorted_logs, 1):
                        status_icon = "⏳" if entry.status == "pending" else "✓"
                        print(f"{i}. [{status_icon}] {entry.priority.upper()} - {entry.description}")
                        print(f"   ID: {entry.id}")
                        print(f"   Creator: {entry.creator} ({entry.creator_role})")
                        if entry.status == "completed":
                            print(f"   Completed by: {entry.completer} ({entry.completer_role})")
                        print()
        
        elif args.command == 'complete':
            # Load logs
            log_dicts = storage.load_logs(DEFAULT_DB_PATH)
            logs = [models.from_dict(d) for d in log_dicts]
            
            # Complete entry
            updated_logs = manager.complete_entry(
                log_id=args.id,
                completer=args.user,
                role=args.role,
                logs=logs
            )
            
            # Save updated logs
            log_dicts = [models.to_dict(entry) for entry in updated_logs]
            storage.save_logs(DEFAULT_DB_PATH, log_dicts)
            
            # Output result
            if args.json:
                result = {
                    "status": "success",
                    "message": f"Entry {args.id} marked as completed"
                }
                json.dump(result, sys.stdout, indent=2)
            else:
                print(f"✓ Entry {args.id} marked as completed by {args.user}")
    
    except ValueError as e:
        # Handle validation errors
        if args.json:
            error = {
                "status": "error",
                "message": str(e)
            }
            json.dump(error, sys.stderr, indent=2)
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    except Exception as e:
        # Handle unexpected errors
        if args.json:
            error = {
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }
            json.dump(error, sys.stderr, indent=2)
        else:
            print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
