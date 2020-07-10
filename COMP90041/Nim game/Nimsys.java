/* *****************************************************************************
 *  Author:     Bingkun Chen
 *  StudentID:  992113
 *  UserName:   BINGKUNC
 *
 *  Description:  This is the class for the main system of Nimsys.
 *                This class is to manage the whole system, and executive
                  input command.
 *
 *  Written:       27/5/2019
 *  Last updated:  31/5/2019
 *
 **************************************************************************** */
 
import java.util.Scanner;
import java.util.ArrayList;
import java.util.InputMismatchException;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.File;
import java.io.FileNotFoundException;

public class Nimsys{
	static Scanner keyboard  = new Scanner(System.in);
    /*
     * Check element's existance.
     * Parameter String[] arr, String value.
     * Return boolean.
     */
	public boolean checkExistance(String[] arr, String value){
		loop:for (int i = 0; i < arr.length; i++){
			if (arr[i] == null){
				break loop;
			}else{ 
				if(arr[i].equals(value))
					return true;
			}
		}
		return false;
	}

    /*
     * Search element's position in the input array.
     * Parameter String[] arr, String value.
     * Return int.
     */
	public int searchPosition(String[] arr, String value){
		
		loop:for (int i = 0; i < arr.length; i++){
			if (arr[i] == null){
				break loop;
			}else{
				if(arr[i].equals(value))
				return i;
			}
		}
		return -1;
	}

    /*
     * Delete array's Element.
     * Parameter String[] arr, int position
     * Return String[].
     */
	public String[] deleteElement(String[] arr, int position){
		if (position < arr.length-1){
			for (int i = position; i < arr.length-1; i++){
				
				arr[i] = arr[i+1];
				arr[i+1] = null;
				
			} return arr;
		} else{
		return arr;
		}
	}

    /*
     * Delete count.
     * Parameter int[] arr, int position.
     * Return int[].
     */
	public int[] deleteCount(int[] arr, int position){
		if (position < arr.length-1){
			for (int i = position; i < arr.length-1; i++){
				arr[i] = arr[i+1];
				arr[i+1] = 0;
			} return arr;
		} else{
		return arr;
		}
	}

    /*
     * Delete winrate.
     * Parameter double[] arr, int position
     * Return double[].
     */
	public double[] deleteWinRate(double[] arr, int position){
		if (position < arr.length-1){
			for (int i = position; i < arr.length-1; i++){
				
				arr[i] = arr[i+1];
				arr[i+1] = 0;
				
			} return arr;
		} else{
		return arr;
		}
	}

    /*
     * Clear Element.
     * Parameter String[] arr.
     * Return String[].
     */
	public String[] clearElement(String[] arr){
		for (int i = 0; i < arr.length; i++){
			arr[i] = null;
		}
		return arr;
	}

    /*
     * Clear count.
     * Parameter int[] arr.
     * Return int[].
     */
	public int[] clearCount(int[] arr){
		for (int i = 0; i < arr.length; i++){
			arr[i] = 0;
		}
		return arr;
	}

    /*
     * Delete count.
     * Parameter double[] arr.
     * Return double[].
     */
	public double[] clearWinRate(double[] arr){
		for (int i = 0; i < arr.length; i++){
			arr[i] = 0;
		}
		return arr;
	}

    /*
     * getRemoveNumber from input.
     * Return int[].
     */
	public int getRemoveNumber(int bound){
		int removeNumber;
		while(true){
			String input =keyboard.next();
			int inputValue = 0;
			try{
				inputValue = Integer.parseInt(input);
				removeNumber = inputValue;
				break;
			}catch(NumberFormatException e){
				System.out.println("Invalid move. You must remove between 1 and " + bound + " stones.");
			}
		}
		keyboard.nextLine();
		return removeNumber;
	}

    /*
     * Calculate winrate.
     * Parameter int[] countOfWin, int[] countOfGames,double[] winRate.
     * Return double[].
     */
	public double[] winRateCalculation(int[] countOfWin, int[] countOfGames,double[] winRate){
		for (int i = 0; i < winRate.length; i++){
			winRate[i] = (double)countOfWin[i] / (double)countOfGames[i];
		}
		return winRate;
	}
	

	public static void main(String[] args){
		String command;

		Nimsys method = new Nimsys();
		PlayerData pd = new PlayerData();
		NimGame game = new NimGame();
		
		// read players.dat.txt
		
		try{
			FileInputStream inputStream = new FileInputStream("players.dat.txt");
			BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
			String line1;
			String line2;
			String line3;
			String line4;
			String line5;
			String line6;
			String line7;
			
			line1 = reader.readLine();
			if (line1 !=null){
				String[] temp1 = line1.split("\t");
				for(int i = 0; i < temp1.length; i++){
					pd.userNameCollection[i] = temp1[i];
				}
			}
			
			line2 = reader.readLine();
			if (line2 !=null){
				String[] temp2 = line2.split("\t");
				for(int i = 0; i < temp2.length; i++){
					pd.familyNameCollection[i] = temp2[i];
				}
			}
			
			line3 = reader.readLine();
			if (line3 !=null){
				String[] temp3 = line3.split("\t");
				for(int i = 0; i < temp3.length; i++){
					pd.givenNameCollection[i] = temp3[i];
				}
			}
			
			line4 = reader.readLine();
			if (line4 !=null){
				String[] temp4 = line4.split("\t");
				for(int i = 0; i < temp4.length; i++){
					pd.countOfWin[i] = Integer.parseInt(temp4[i], 10);
				}
			}
			
			line5 = reader.readLine();
			if (line5 !=null){
				String[] temp5 = line5.split("\t");
				for(int i = 0; i < temp5.length; i++){
					pd.countOfGames[i] = Integer.parseInt(temp5[i], 10);
				}
			}
			
			line6 = reader.readLine();
			if (line6 !=null){
				String[] temp6 = line6.split("\t");
				for(int i = 0; i < temp6.length; i++){
					pd.winRate[i] = Double.parseDouble(temp6[i]);
				}
			}
			
			line7 = reader.readLine();
			if (line7 !=null){
				String[] temp7 = line7.split("\t");
				for(int i = 0; i < temp7.length; i++){
					(pd.aiUserName).add(temp7[i]);
				}
			}
			inputStream.close();
			reader.close();
		}catch(FileNotFoundException e){
			
		}catch(IOException e){
			e.printStackTrace();
		}

		int flag = 0; 

		System.out.println("Welcome to Nim");
		
		while (flag == 0){
			System.out.println();
			System.out.print("$");
			String input = keyboard.nextLine();
			
			String[]temp = input.split(" ");
			command = temp[0];
			
			try {
				if (!command.equals("addplayer") &&
					!command.equals("addaiplayer") &&
					!command.equals("editplayer") &&
					!command.equals("startgame") &&
					!command.equals("removeplayer") &&
					!command.equals("resetstats") &&
					!command.equals("rankings") &&
					!command.equals("displayplayer") &&
					!command.equals("rankings") &&
					!command.equals("exit")){
						
						throw new CommandException(" is not a valid command.");
					}
			}catch (CommandException c){
				
				System.out.println("'" + command + "'" + c.getMessage());
			}
			
			try {
				if (command.equals("addplayer") && !input.contains(",")){
					
					throw new ArgumentException("Incorrect number of arguments supplied to command.");
					
				} else if (command.equals("addaiplayer") && !input.contains(",")){
					
					throw new ArgumentException("Incorrect number of arguments supplied to command.");
					
				} else if (command.equals("editplayer") && !input.contains(",")){
					
					throw new ArgumentException("Incorrect number of arguments supplied to command.");
					
				} else if (command.equals("startgame") && !input.contains(",")){
					
					throw new ArgumentException("Incorrect number of arguments supplied to command.");
				}
			}catch (ArgumentException a){
				
				System.out.println(a.getMessage());
			}
			

			if (input.contains(" ") && input.contains(",")){
				
				try {
					String[]information = temp[1].split(",", 4);
					
					if (command.equals("addplayer")){
						
						String userName = information[0];
						String familyName = information[1];
						String givenName = information[2];
						
						boolean existance = method.checkExistance(pd.userNameCollection,userName);
					
						if (existance){
							System.out.println("The player already exists.");
						} else {
							loop:for (int i = 0; i < (pd.userNameCollection).length; i++){
								if (pd.userNameCollection[i] == null){
									pd.userNameCollection[i] = userName;
									pd.familyNameCollection[i] = familyName;
									pd.givenNameCollection[i] = givenName;
									
									break loop;
								}
							}
						}
					} else if(command.equals("addaiplayer")){
						String userName = information[0];
						String familyName = information[1];
						String givenName = information[2];
						
						boolean existance = method.checkExistance(pd.userNameCollection,userName);
					
						if (existance){
							System.out.println("The player already exists.");
						} else {
							loop:for (int i = 0; i < (pd.userNameCollection).length; i++){
								if (pd.userNameCollection[i] == null){
									pd.userNameCollection[i] = userName;
									pd.familyNameCollection[i] = familyName;
									pd.givenNameCollection[i] = givenName;
									(pd.aiUserName).add(userName);
									
									break loop;
								}
							}
						}
						
					} else if(command.equals("editplayer")){
						String userName = information[0];
						String familyName = information[1];
						String givenName = information[2];
						
						boolean existance = method.checkExistance(pd.userNameCollection,userName);
						
						if(!existance){
							System.out.println("The player does not exist.");
						} else {
						int position = method.searchPosition(pd.userNameCollection,userName);
						
						pd.familyNameCollection[position] = familyName;
						pd.givenNameCollection[position] = givenName;
						
						}
					} else if (command.equals("startgame")){
						
						String user1 = information[2];
						String user2 = information[3];
						
						boolean user1Existance = method.checkExistance(pd.userNameCollection,user1);
						boolean user2Existance = method.checkExistance(pd.userNameCollection,user2);
						
						if(user1Existance && user2Existance){
							int index1 = method.searchPosition(pd.userNameCollection, user1);
							int index2 = method.searchPosition(pd.userNameCollection, user2);
							
							game.indexOfPlayer1 = index1;
							game.indexOfPlayer2 = index2;
							game.aiCheck1 = (pd.aiUserName).contains(user1);
							game.aiCheck2 = (pd.aiUserName).contains(user2);
							
							game.info1 = pd.userNameCollection;
							game.info2 = pd.familyNameCollection;
							game.info3 = pd.givenNameCollection;
							game.playerData1 = pd.countOfGames;
							game.playerData2 = pd.countOfWin;
							
							String initialStone = information[0];
							Integer integer1 = new Integer(initialStone);
							game.initialStone = integer1.intValue();
							
							String upperBound = information[1];
							Integer integer2 = new Integer(upperBound);
							game.removalUpperBound = integer2.intValue();
							
							int[] dataCollection = new int[6];
							dataCollection = game.runGame(game.initialStone,game.removalUpperBound,user1,user2);
							
							int p1 = dataCollection[0];
							pd.countOfWin[p1] = dataCollection[1];
							pd.countOfGames[p1] = dataCollection[2];
							
							int p2 = dataCollection[3];
							pd.countOfWin[p2] = dataCollection[4];
							pd.countOfGames[p2] = dataCollection[5];
							
							pd.winRate = method.winRateCalculation(pd.countOfWin,pd.countOfGames,pd.winRate);
							
						} else {
							System.out.println("One of the players does not exist.");
						}
					} 
				}catch (ArrayIndexOutOfBoundsException e){
					
					System.out.println("Incorrect number of arguments supplied to command.");
				}
			
			} else if(input.contains(" ") && !input.contains(",")){
				try{
					String userName = temp[1];
					
					if (command.equals("removeplayer")){
						
						boolean existance = method.checkExistance(pd.userNameCollection,userName);
						
						if(!existance){
							System.out.println("The player does not exist.");
						} else {
							int position = method.searchPosition(pd.userNameCollection,userName);
							
							pd.userNameCollection = method.deleteElement(pd.userNameCollection,position);
							pd.familyNameCollection = method.deleteElement(pd.familyNameCollection,position);
							pd.givenNameCollection = method.deleteElement(pd.givenNameCollection,position);
							pd.countOfWin = method.deleteCount(pd.countOfWin,position);
							pd.countOfGames = method.deleteCount(pd.countOfGames,position);
							pd.winRate = method.deleteWinRate(pd.winRate,position);
							if ( (pd.aiUserName).contains(userName) ){
								(pd.aiUserName).remove(userName);
							}
							
						}
					} else if (command.equals("resetstats")){
						
						boolean existance = method.checkExistance(pd.userNameCollection,userName);
						
						if(!existance){
							System.out.println("The player does not exist.");
						} else {
							int position = method.searchPosition(pd.userNameCollection,userName);
							
							pd.countOfWin[position] = 0;
							pd.countOfGames[position] = 0;
							pd.winRate[position] = 0;
						}
					} else if (command.equals("rankings")){
						String order = temp[1];
						
						if(order.equals("asc")){
							
							pd.rankingsAsc();
							
						} else {
							
							pd.rankingsDesc();
						}
					} else if (command.equals("displayplayer")){
						
						boolean existance = method.checkExistance(pd.userNameCollection,userName);
						
						if(!existance){
							System.out.println("The player does not exist.");
							
						} else if (existance){
							int index = method.searchPosition(pd.userNameCollection,userName);
							pd.displayPlayer(index);
						}
					}
				}catch (ArrayIndexOutOfBoundsException e){
					
					System.out.println("Incorrect number of arguments supplied to command.");
				}
			
			}else if (!input.contains(" ")){
				if (command.equals("displayplayer")){
					pd.displayAllPlayer();
				} else if (command.equals("removeplayer")){
					System.out.println("Are you sure you want to remove all players? (y/n)");
					String answer = keyboard.nextLine();
					
					if (answer.equalsIgnoreCase("y")){
						pd.userNameCollection = method.clearElement(pd.userNameCollection);
						pd.familyNameCollection = method.clearElement(pd.familyNameCollection);
						pd.givenNameCollection = method.clearElement(pd.givenNameCollection);
						pd.countOfWin = method.clearCount(pd.countOfWin);
						pd.countOfGames = method.clearCount(pd.countOfGames);
						pd.winRate = method.clearWinRate(pd.winRate);
						(pd.aiUserName).clear();
					}
				} else if (command.equals("resetstats")){
					System.out.println("Are you sure you want to reset all player statistics? (y/n)");
					String answer = keyboard.nextLine();
					
					if (answer.equalsIgnoreCase("y")){
						pd.countOfWin = method.clearCount(pd.countOfWin);
						pd.countOfGames = method.clearCount(pd.countOfGames);
						pd.winRate = method.clearWinRate(pd.winRate);
					}
				} else if (command.equals("rankings")){
					
					pd.rankingsDesc();
					
				} else if (command.equals("exit")){
					// Save players.dat
					
					int n = 0;
					for(int i = 0; i < 100; i++){
						if (pd.userNameCollection[i] == null){
							n = i;
							break;
						}
					}
					File f = new File("players.dat.txt");
					FileWriter fw = null;
					try{
						
						fw = new FileWriter(f);
						for(int i = 0; i < n; i++){
							fw.write(pd.userNameCollection[i] + "\t");
						}
						
						fw.flush();
						fw.write("\r\n");
						for(int i = 0; i < n; i++){
							fw.write(pd.familyNameCollection[i] + "\t");
						}
						
						fw.flush();
						fw.write("\r\n");
						
						for(int i = 0; i < n; i++){
							fw.write(pd.givenNameCollection[i] + "\t");
						}
						
						fw.flush();
						fw.write("\r\n");
						
						for(int i = 0; i < n; i++){
							fw.write(pd.countOfWin[i] + "\t");
						}
						
						fw.flush();
						fw.write("\r\n");
						
						for(int i = 0; i < n; i++){
							fw.write(pd.countOfGames[i] + "\t");
						}
						
						fw.flush();
						fw.write("\r\n");
						
						for(int i = 0; i < n; i++){
							fw.write(pd.winRate[i] + "\t");
						}
						
						fw.flush();
						fw.write("\r\n");
						
						for(int i = 0; i < (pd.aiUserName).size(); i++){
							String str = (pd.aiUserName).get(i);
							fw.write(str + "\t");
						}
						
					}catch(IOException e){
						e.printStackTrace();
					}finally{
						try{
							fw.close();
						}catch(IOException e){
						e.printStackTrace();
						}
					}
					
					System.out.println();
					System.exit(0);
				}
			}
			
		}
		
		
	
	}
}