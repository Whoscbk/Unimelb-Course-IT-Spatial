/* *****************************************************************************
 *  Author:     Bingkun Chen
 *  StudentID:  992113
 *  UserName:   BINGKUNC
 *
 *  Description:  This is the class for NimHumanPlayer.
 *
 *  Written:       27/5/2019
 *  Last updated:  31/5/2019
 *
 **************************************************************************** */
 
class NimHumanPlayer extends NimPlayer{
	
	public int removeStone(int flag, int bound, int initialNum, int currentNum){
		
		Nimsys nim = new Nimsys();
		int removeNumber = nim.getRemoveNumber(bound);
		return removeNumber;
	}
}