/* *****************************************************************************
 *  Author:     Bingkun Chen
 *  StudentID:  992113
 *  UserName:   BINGKUNC
 *
 *  Description:  This is the class for Nimgame.
 *                This class is to manage the whole game playing process.
 *
 *  Written:       27/5/2019
 *  Last updated:  31/5/2019
 *
 **************************************************************************** */

class NimGame{
	
	int initialStone;
	int currentStone;
	int removalUpperBound;
	int indexOfPlayer1;
	int indexOfPlayer2;
	boolean aiCheck1;
	boolean aiCheck2;
	
	String[] info1 = new String [100];
	String[] info2 = new String [100];
	String[] info3 = new String [100];

	int[] playerData1 = new int [100];
	int[] playerData2 = new int [100];
	
	NimPlayer player1 = null;
	NimPlayer player2 = null;
	
	
	
    /**
     * Print the number of stones left.
     * Display the stones by asterisks.
     * Parameter numberOfStones.
     * Return void.
     */
	public void printStones(int numberOfStones){
		int i;
		
		System.out.println();
		System.out.print(numberOfStones + " stones left:");
		for (i = 0; i < numberOfStones; i++){
			System.out.print(" *");
		}
		System.out.println();
	}
	
    /**
     * Check the validity of the removeNumber each turn.
     * Parameter int removeNumber, int currentNumber, int upperBound
     * Return boolean.
     */
	public boolean checkStoneNumber(int removeNumber, int currentNumber, int upperBound){
		if (removeNumber > 0 && removeNumber <= upperBound && removeNumber <= currentNumber){
			return true;
		} else {
			return false;
		}
	}

    /**
     * Manage the game process.
     * Parameter int initialStone,int maxmumRemoval,String userName1,String userName2.
     * Return int[].
     */
	public int[] runGame(int initialStone,int maxmumRemoval,String userName1,String userName2){
		
		currentStone = initialStone;
		
		Nimsys nimsys = new Nimsys();
		int mark1 = 0;
		int mark2 = 0;
		
		if(aiCheck1){
			player1 = new NimAIPlayer();
			mark1 = 1;
		} else {
			player1 = new NimHumanPlayer();
		}
		
		if(aiCheck2){
			player2 = new NimAIPlayer();
			mark2 = 2;
		} else {
			player2 = new NimHumanPlayer();
		}
		
		player1.setGamePlayerInfo(indexOfPlayer1, info1, info2, info3);
		player1.setGamePlayerData(indexOfPlayer1, playerData1, playerData2);
		
		player2.setGamePlayerInfo(indexOfPlayer2, info1, info2, info3);
		player2.setGamePlayerData(indexOfPlayer2, playerData1, playerData2);
		
		int[] data = new int[6];
		data[0] = indexOfPlayer1;
		data[1] = player1.winCount;
		data[2] = player1.gameCount;
		data[3] = indexOfPlayer2;
		data[4] = player2.winCount;
		data[5] = player2.gameCount;

		int turn = 1;
		
		System.out.println();
		System.out.println("Initial stone count: " + initialStone);
		System.out.println("Maximum stone removal: " + maxmumRemoval);
		System.out.println("Player 1: " + player1.givenName + " " + player1.familyName);
		System.out.println("Player 2: " + player2.givenName + " " + player2.familyName);


		while (currentStone != 0){
			if (turn % 2 == 1){
				int num;
				if (currentStone != removalUpperBound){
					num = Math.min(currentStone, removalUpperBound);
				} else {
					num = removalUpperBound;
				}
				
				try{
					if (currentStone > 0){
						printStones(currentStone);
					}
					System.out.println(player1.givenName + "'s turn - remove how many?");

					int removeStone = player1.removeStone(mark1, removalUpperBound, initialStone,currentStone);
					boolean flag = checkStoneNumber(removeStone,currentStone,removalUpperBound);
					
					if (!flag){
						throw new MoveException("Invalid move. You must remove between 1 and ");
					}
					
					currentStone -= removeStone;
					turn++;
				}catch (MoveException m){
					System.out.println();
					System.out.println(m.getMessage() + num + " stones.");
				}
			} else {
				int num;
				if (currentStone != removalUpperBound){
					num = Math.min(currentStone, removalUpperBound);
				} else {
					num = removalUpperBound;
				}
				
				try{
					if (currentStone > 0){
						printStones(currentStone);
					}
					System.out.println(player2.givenName + "'s turn - remove how many?");
					
					
					int removeStone = player2.removeStone(mark1, removalUpperBound, initialStone,currentStone);
					boolean flag = checkStoneNumber(removeStone,currentStone,removalUpperBound);
						
					if (!flag){
						throw new MoveException("Invalid move. You must remove between 1 and ");
					}
						
					currentStone -= removeStone;
					turn++;
				}catch (MoveException m){
					System.out.println();
					System.out.println(m.getMessage() + num + " stones.");
				}
			}
		}
		
		
		System.out.println();
		System.out.println("Game Over");

		if (turn % 2 == 1){
			data[1] += 1;
			data[2] += 1;
			data[5] += 1;
			System.out.println(player1.givenName + " " + player1.familyName + " wins!");
			return data;
		} else {
			data[4] += 1;
			data[2] += 1;
			data[5] += 1;
			System.out.println(player2.givenName + " " + player2.familyName + " wins!");
			return data;
		}
	}
}