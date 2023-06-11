package randomrandom;

import java.awt.BorderLayout;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;

public class sudokusolver extends JFrame {

	private static final int GRID_SIZE = 9;
	private JTextField[][] textFieldGrid;
	private JButton solveButton;

	public sudokusolver() {
		setTitle("Sudoku Solver");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setLayout(new BorderLayout());
		initializeTextFieldGrid();
		add(textFieldGridPanel(), BorderLayout.CENTER);
		add(solveButton(), BorderLayout.SOUTH);
		pack();
		setLocationRelativeTo(null);
		setVisible(true);
	}

	private void initializeTextFieldGrid() {
		textFieldGrid = new JTextField[GRID_SIZE][GRID_SIZE];
		for (int i = 0; i < GRID_SIZE; i++) {
			for (int j = 0; j < GRID_SIZE; j++) {
				textFieldGrid[i][j] = new JTextField(1);
				textFieldGrid[i][j].setHorizontalAlignment(JTextField.CENTER);
			}
		}
	}

	private JPanel textFieldGridPanel() {
		JPanel panel = new JPanel(new GridLayout(GRID_SIZE, GRID_SIZE));
		for (int i = 0; i < GRID_SIZE; i++) {
			for (int j = 0; j < GRID_SIZE; j++) {
				panel.add(textFieldGrid[i][j]);
			}
		}
		return panel;
	}

	private JButton solveButton() {
		solveButton = new JButton("Solve");
		solveButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				int[][] board = getBoardFromTextFields();
				if (solver(board)) {
					JOptionPane.showMessageDialog(null, "Solved successfully!");
				} else {
					JOptionPane.showMessageDialog(null, "Unsolvable board.");
				}
				updateTextFields(board);
			}
		});
		return solveButton;
	}

	private int[][] getBoardFromTextFields() {
		int[][] board = new int[GRID_SIZE][GRID_SIZE];
		for (int i = 0; i < GRID_SIZE; i++) {
			for (int j = 0; j < GRID_SIZE; j++) {
				String text = textFieldGrid[i][j].getText();
				try {
					int number = Integer.parseInt(text);
					board[i][j] = number;
				} catch (NumberFormatException e) {
					board[i][j] = 0;
				}
			}
		}
		return board;
	}

	private void updateTextFields(int[][] board) {
		for (int i = 0; i < GRID_SIZE; i++) {
			for (int j = 0; j < GRID_SIZE; j++) {
				textFieldGrid[i][j].setText(Integer.toString(board[i][j]));
			}
		}
	}

	public static void main(String[] args) {
		SwingUtilities.invokeLater(new Runnable() {
			public void run() {
				new sudokusolver();
			}
		});
	}

	private static boolean solver(int[][] board) {
		for (int i = 0; i < GRID_SIZE; i++) {
			for (int j = 0; j < GRID_SIZE; j++) {
				if (board[i][j] == 0) {
					for (int num = 1; num <= GRID_SIZE; num++) {
						if (isValidPlacement(board, num, i, j)) {
							board[i][j] = num;

							if (solver(board)) {
								return true;
							} else {
								board[i][j] = 0;
							}
						}
					}
					return false;
				}
			}
		}

		return true;

	}

	private static boolean isNumberInRow(int[][] board, int number, int row) {
		for (int i = 0; i < GRID_SIZE; i++) {
			if (board[row][i] == number) {
				return true;
			}
		}

		return false;
	}

	private static boolean isNumberInCol(int[][] board, int number, int col) {
		for (int i = 0; i < GRID_SIZE; i++) {
			if (board[i][col] == number) {
				return true;
			}
		}

		return false;
	}

	private static boolean isNumberInBox(int[][] board, int number, int row, int col) {
		int localBoxRow = row - row % 3;
		int localBoxColumn = col - col % 3;

		for (int i = localBoxRow; i < localBoxRow + 3; i++) {
			for (int j = localBoxColumn; j < localBoxColumn + 3; j++) {
				if (board[i][j] == number) {
					return true;
				}
			}

		}

		return false;
	}

	private static boolean isValidPlacement(int[][] board, int number, int row, int col) {
		return !isNumberInRow(board, number, row) && !isNumberInCol(board, number, col)
				&& !isNumberInBox(board, number, row, col);
	}
}