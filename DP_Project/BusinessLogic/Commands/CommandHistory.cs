using System;
using System.Collections.Generic;

public class CommandHistory
{
    private readonly Stack<ICommand> _undoStack = new();
    private readonly Stack<ICommand> _redoStack = new();

    public void ExecuteCommand(ICommand command)
    {
        if (command.Execute())
        {
            _undoStack.Push(command);
            _redoStack.Clear();
        }
    }

    public bool Undo()
    {
        if (_undoStack.Count == 0) return false;
        
        var command = _undoStack.Pop();
        if (command.Undo())
        {
            _redoStack.Push(command);
            return true;
        }
        return false;
    }

    public bool Redo()
    {
        if (_redoStack.Count == 0) return false;

        var command = _redoStack.Pop();
        if (command.Execute())
        {
            _undoStack.Push(command);
            return true;
        }
        return false;
    }
} 