/*
	NimAIPlayer.java
	
	This class is provided as a skeleton code for the tasks of 
	Sections 2.4, 2.5 and 2.6 in Project C. Add code (do NOT delete any) to it
	to finish the tasks. 
*/

public class NimAIPlayer extends NimPlayer implements Testable{
	// you may further extend a class or implement an interface
	// to accomplish the tasks.	

	public NimAIPlayer() {
				
	}
	
	public String advancedMove(boolean[] available, String lastMove) {
		// the implementation of the victory
		// guaranteed strategy designed by you
		String move = "";
		
		return move;
	}
	
	public int removeStone(int flag, int bound, int initialNum, int currentNum){
		int position = flag;
		int max = bound;
		int initCheck = 0;
		int currentCheck = 0;
		int removeNumber = 0;
		int randomNum = 0;
		
		loop:for (int k = 0; k < initialNum; k++){
			if((k*(max+1))+1 == initialNum){
				initCheck = 1;
				
				break loop;
			} else {
				initCheck = -1;
			}
		}
		
		for (int i = 1; i <= max; i++){
			int nextNum = currentNum - i;
			loop:for (int k = 0; k < currentNum; k++){
				if ((k*(max+1))+1 == nextNum){
					removeNumber = i;
					currentCheck = 1;
					
					break loop;
				} else {
					int a;
					if (max <= currentNum){
						a = max;
					} else {
						a = currentNum;
					}
					
					randomNum = 1 + (int)(Math.random()*a);
					currentCheck = -1;
				}
			}
		}
		
		
		if (initCheck == 1 && position == 2){

			return removeNumber;
			
		} else if (initCheck == -1 && position == 1){
			
			return removeNumber;
			
		} else if (currentCheck == 1){
			
			return removeNumber;
			
		} else {
			if (removeNumber != 0){
				
				return removeNumber;
				
			} else {
				
				return randomNum;
			}
			
		}
	}
}
