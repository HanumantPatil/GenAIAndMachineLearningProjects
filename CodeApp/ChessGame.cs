using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
/*
 * 
 * Funtional requirements:
 * 
 * 1. Chess Game
 * 2. Two Players
 * 3. Chess Board
 * 4. Chess Pieces
 * 5. Move Validation
 * 6. Check and Checkmate Detection
 * 7. Turn Management
 * 8. Game State Management (e.g., ongoing, draw, win)
 * 
 * 8*8 (i,j)
 * 
 * 
 * 
 */
namespace CodeApp
{
    public class Position
    {
        public int X { get; set; }
        public int Y { get; set; }
    }
    public enum PieceType
    {
        Pawn,
        Rook,
        Knight,
        Bishop,
        Queen,
        King
    }
    public enum GameState
    {
        Ongoing,
        Draw,
        WhiteWin,
        BlackWin
    }
    public enum Color
    {
        White,
        Black
    }
    public enum MoveResult
    {
        Valid,
        Invalid,
        Check,
        Checkmate
    }
    public enum GameStatus
    {
        Ongoing,
        Draw,
        WhiteWin,
        BlackWin
    }
    public abstract class ChessPiece
    {
        public PieceType Type { get; set; }
        public Position Position { get; set; }
        public Color Color { get; set; }
        public abstract bool IsValidMove(Position newPosition, ChessBoard board);
    }
    public class ChessBoard
    {
        public ChessPiece[,] Board { get; set; } = new ChessPiece[8, 8];
    }
    internal class ChessGame
    {
        public ChessBoard Board { get; set; } = new ChessBoard();
        public bool IsWhiteTurn { get; set; } = true;
    }
   public class King : ChessPiece
    {
        public override bool IsValidMove(Position newPosition, ChessBoard board)
        {
            // Implement King move validation logic
            return true;
        }
    }
    public class Queen : ChessPiece
    {
        public override bool IsValidMove(Position newPosition, ChessBoard board)
        {
            // Implement Queen move validation logic
            return true;
        }
    }
    public class Rook : ChessPiece
    {
        public override bool IsValidMove(Position newPosition, ChessBoard board)
        {
            // Implement Rook move validation logic
            return true;
        }
    }
    public class Bishop : ChessPiece
    {
        public override bool IsValidMove(Position newPosition, ChessBoard board)
        {
            // Implement Bishop move validation logic
            return true;
        }
    }
    public class Knight : ChessPiece
    {
        public override bool IsValidMove(Position newPosition, ChessBoard board)
        {
            // Implement Knight move validation logic
            return true;
        }
    }
    public class Pawn : ChessPiece
    {
        public override bool IsValidMove(Position newPosition, ChessBoard board)
        {
            // Implement Pawn move validation logic
            return true;
        }
    }
    public class  Cell
    {
        
    }

}
