/* *****************************************************************************
 *  Author:     Bingkun Chen
 *  StudentID:  992113
 *  UserName:   BINGKUNC
 *
 *  Description:  This is the class for NimPlayer.
 *
 *  Written:       27/5/2019
 *  Last updated:  31/5/2019
 *
 **************************************************************************** */

abstract class NimPlayer{
	
	String userName;
	String givenName;
	String familyName;
	int gameCount;
	int winCount;
	
	public void setGamePlayerInfo(int i, String[] arr1, String[] arr2, String[] arr3){
		userName = arr1[i];
		familyName = arr2[i];
		givenName = arr3[i];
	}
	
	public void setGamePlayerData(int i, int[] count1, int[] count2){
		gameCount = count1[i];
		winCount = count2[i];
	}
	
	public abstract int removeStone(int flag, int bound, int initialNum, int currentNum);
	
}