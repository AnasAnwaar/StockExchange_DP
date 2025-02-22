public interface ICommand
{
    bool Execute();
    bool Undo();
    string GetDescription();
}