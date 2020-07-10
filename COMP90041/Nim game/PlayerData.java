/* *****************************************************************************
 *  Author:     Bingkun Chen
 *  StudentID:  992113
 *  UserName:   BINGKUNC
 *
 *  Description:  This is the class for PlayerDatas.
 *                This class contains the information of each Player's Data.
 *
 *  Written:       27/5/2019
 *  Last updated:  31/5/2019
 *
 **************************************************************************** */
 
import java.util.ArrayList;
class PlayerData{

	String[] userNameCollection = new String [100];
	String[] familyNameCollection = new String [100];
	String[] givenNameCollection = new String [100];
	ArrayList<String> aiUserName = new ArrayList<String>();

	int[] countOfWin = new int [100];
	int[] countOfGames = new int [100];
	double[] winRate = new double [100];
	

    /*
     * Display Single user.
     * Parameter int i.
     * Return void.
     */
	public void displayPlayer(int i){
		System.out.println(userNameCollection[i] + "," + givenNameCollection[i] + "," + 
			familyNameCollection[i] + ","+ countOfGames[i] + " games,"+ countOfWin[i] + " wins");
	}

    /*
     * Used for String array copy.
     * Parameter String[] arr, String[] copy.
     * Return String[].
     */
	public String[] stringCopy(String[] arr, String[] copy){
		for (int i = 0; i < arr.length; i++){
			copy[i] = arr[i];
		}
		return copy;
	}

    /*
     * Used for int array copy.
     * Parameter int[] arr, int[] copy.
     * Return int[].
     */
	public int[] intCopy(int[] arr, int[] copy){
		for (int i = 0; i < arr.length; i++){
			copy[i] = arr[i];
		}
		return copy;
	}

    /*
     * Used for double array copy.
     * Parameter double[] arr, double[] copy.
     * Return double[].
     */
	public double[] doubleCopy(double[] arr, double[] copy){
		for (int i = 0; i < arr.length; i++){
			copy[i] = arr[i];
		}
		return copy;
	}
	
    /*
     * Display All user alphabetically.
     * Return void.
     */
	public void displayAllPlayer(){
		String[] a1 = new String [100];
		String[] a2 = new String [100];
		String[] a3 = new String [100];
		int[] a4 = new int [100];
		int[] a5 = new int [100];
		
		stringCopy(userNameCollection, a1);
		stringCopy(givenNameCollection, a2);
		stringCopy(familyNameCollection, a3);
		intCopy(countOfGames, a4);
		intCopy(countOfWin, a5);
		
		for (int i = 0; i < a1.length-1; i++){
			for (int j = i+1; j < a1.length-1; j++){
				if (a1[j] == null){
					break;
				} else if (a1[i].compareTo(a1[j]) > 0){
					String temp1 = a1[i];
					String temp2 = a2[i];
					String temp3 = a3[i];
					int temp4 = a4[i];
					int temp5 = a5[i];
					
					a1[i] = a1[j];
					a2[i] = a2[j];
					a3[i] = a3[j];
					a4[i] = a4[j];
					a5[i] = a5[j];
					
					a1[j] = temp1;
					a2[j] = temp2;
					a3[j] = temp3;
					a4[j] = temp4;
					a5[j] = temp5;
				} else {
					continue;
				}
			}
		}
		loop:for (int i = 0; i < a1.length-1; i++){
			if (a1[i] == null){
				break loop;
			} else {
				System.out.println(a1[i] + "," + a2[i] + "," + a3[i] + ","
					+ a4[i] + " games,"+ a5[i] + " wins");
			}
		}
	}

    /*
     * Display rankings asc.
     * Return void.
     */
	public void rankingsAsc(){
		String[] a1 = new String [100];
		int[] a2 = new int [100];
		double[] a3 = new double [100];
		String[] a4 = new String [100];
		String[] a5 = new String [100];
		
		stringCopy(userNameCollection, a1);
		intCopy(countOfGames, a2);
		doubleCopy(winRate, a3);
		stringCopy(givenNameCollection, a4);
		stringCopy(familyNameCollection, a5);
		
		for (int i = 0; i < a3.length-1; i++){
			for (int j = i+1; j < a3.length-1; j++){
				if (a1[j] == null){
					break;
				} else if (a3[i] > a3[j]){
					String temp1 = a1[i];
					int temp2 = a2[i];
					double temp3 = a3[i];
					String temp4 = a4[i];
					String temp5 = a5[i];
					
					a1[i] = a1[j];
					a2[i] = a2[j];
					a3[i] = a3[j];
					a4[i] = a4[j];
					a5[i] = a5[j];
					
					a1[j] = temp1;
					a2[j] = temp2;
					a3[j] = temp3;
					a4[j] = temp4;
					a5[j] = temp5;
					
				} else if (a3[i] == a3[j]){
					if (a1[i].compareTo(a1[j]) > 0){
						String temp1 = a1[i];
						int temp2 = a2[i];
						double temp3 = a3[i];
						String temp4 = a4[i];
						String temp5 = a5[i];
					
						a1[i] = a1[j];
						a2[i] = a2[j];
						a3[i] = a3[j];
						a4[i] = a4[j];
						a5[i] = a5[j];
					
						a1[j] = temp1;
						a2[j] = temp2;
						a3[j] = temp3;
						a4[j] = temp4;
						a5[j] = temp5;
					}
				}
			}
		}
		loop:for (int i = 0; i < 10; i++){
			if (a1[i] == null){
				break loop;
			} else {
				
				System.out.println(String.format("%-5S",Math.round(a3[i] * 100) + "%") + "| " 
				+ String.format("%02d",a2[i]) + " games | " + a4[i] + " " + a5[i]);
			}
		}
	}
	
    /*
     * Display rankings desc.
     * Return void.
     */
	public void rankingsDesc(){
		String[] a1 = new String [100];
		int[] a2 = new int [100];
		double[] a3 = new double [100];
		String[] a4 = new String [100];
		String[] a5 = new String [100];
		
		stringCopy(userNameCollection, a1);
		intCopy(countOfGames, a2);
		doubleCopy(winRate, a3);
		stringCopy(givenNameCollection, a4);
		stringCopy(familyNameCollection, a5);
		
		for (int i = 0; i < a3.length-1; i++){
			for (int j = i+1; j < a3.length-1; j++){
				if (a1[j] == null){
					break;
				} else if (a3[i] < a3[j]){
					String temp1 = a1[i];
					int temp2 = a2[i];
					double temp3 = a3[i];
					String temp4 = a4[i];
					String temp5 = a5[i];
					
					a1[i] = a1[j];
					a2[i] = a2[j];
					a3[i] = a3[j];
					a4[i] = a4[j];
					a5[i] = a5[j];
					
					a1[j] = temp1;
					a2[j] = temp2;
					a3[j] = temp3;
					a4[j] = temp4;
					a5[j] = temp5;
					
				} else if (a3[i] == a3[j]){
					if (a1[i].compareTo(a1[j]) > 0){
						String temp1 = a1[i];
						int temp2 = a2[i];
						double temp3 = a3[i];
						String temp4 = a4[i];
						String temp5 = a5[i];
					
						a1[i] = a1[j];
						a2[i] = a2[j];
						a3[i] = a3[j];
						a4[i] = a4[j];
						a5[i] = a5[j];
					
						a1[j] = temp1;
						a2[j] = temp2;
						a3[j] = temp3;
						a4[j] = temp4;
						a5[j] = temp5;
					}
				} else if (a3[i] > a3[j]){
					continue;
				}
			}
		}
		loop:for (int i = 0; i < 10; i++){
			if (a1[i] == null){
				break loop;
			} else {
				
				System.out.println(String.format("%-5S",Math.round(a3[i] * 100) + "%") + "| " 
				+ String.format("%02d",a2[i]) + " games | " + a4[i] + " " + a5[i]);
			}
		}
	}
}