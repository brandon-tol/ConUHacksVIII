package src;
import java.util.Scanner;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;

public interface CSVParser {
    public static ArrayList<Row> parse(String filename) throws FileNotFoundException, IOException
    {
        Scanner sc = new Scanner(new FileInputStream(filename));
        Scanner line = null;
        ArrayList<Row> list = new ArrayList<>();
        // FIXME: skip the first line if its heading the columns
        sc.nextLine();
        while(sc.hasNextLine()) {
            // TODO: Check for parsing exceptions
            line = new Scanner(sc.nextLine());
            line.useDelimiter(",");
            String matchID = line.next();
            String[] time = line.next().split(":");
            int startTime = Integer.parseInt(time[0]) * 3600 + Integer.parseInt(time[1]) * 60 + Integer.parseInt(time[2]);
            Day dayOfWeek = convertStringToDay(line.next());
            boolean killer = "KILLER".equals(fixString(line.next()));
            int partySize = Integer.parseInt(line.next());
            Server server = convertStringToServer(line.next());
            Platform platform = convertStringToPlatform(line.next());
            long queueDuration = Long.parseLong(line.next());
            MatchmakingOutcome mmOutcome = convertStringToMatchmakingOutcome(line.next());
            int mmr = Integer.parseInt(line.next());
            String characterName = line.next();
            line.close();
            list.add(new Row(matchID, startTime, dayOfWeek, killer, partySize, server, platform, queueDuration, mmOutcome, mmr, characterName));
        }
        sc.close();
        return list;
    }


    private static Day convertStringToDay(String input) {
        try {
            return Day.valueOf(fixString(input));
        } catch (IllegalArgumentException e) {
            return Day.UNKNOWN; // Or return a default value
        }
    }
    
    private static Server convertStringToServer(String input) {
        try {
            return Server.valueOf(fixString(input));
        } catch (IllegalArgumentException e) {
            return Server.UNKNOWN; // Or return a default value
        }
    }
    
    private static Platform convertStringToPlatform(String input) {
        try {
            return Platform.valueOf(fixString(input));
        } catch (IllegalArgumentException e) {
            return Platform.UNKNOWN; // Or return a default value
        }
    }
    
    private static MatchmakingOutcome convertStringToMatchmakingOutcome(String input) {
        try {
            return MatchmakingOutcome.valueOf(fixString(input));
        } catch (IllegalArgumentException e) {
            return MatchmakingOutcome.UNKNOWN;
        }
    }

    private static String fixString(String input) {
        return input.toUpperCase().replace("-", "_");
    }
    


}
