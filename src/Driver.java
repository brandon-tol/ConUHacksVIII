package src;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;


public class Driver {

    static double[] weights = new double[4];

    public static double getDistanceToRow(Row r1, Row r2)
    {
        if(r2.mmOutcome() != MatchmakingOutcome.SUCCESS || r1.serverName() != r2.serverName())
            return Double.POSITIVE_INFINITY;
        return Math.sqrt(weights[0] * (Math.pow(r1.startTime() - r2.startTime(), 2)) + weights[1] * Math.pow(r1.partySize() - r2.partySize(), 2) + weights[2] * Math.pow(r1.mmr() + r2.mmr(), 2) + weights[3] * ((r1.killer() == r2.killer()) ? 1 : 0));
    }

    public static long queueTime(Row r, ArrayList<Row> rows) {
        Comparator<Row> comp = Comparator.comparingDouble(row -> {
            return getDistanceToRow(r, row);
        });

        Collections.sort(rows, comp);
        return rows.get(0).queueDuration();
    } 

    public static void main(String[] args) throws IOException {
        weights[0] = 0;
        weights[1] = 1;
        weights[2] = 100;
        weights[3] = 1;

        var x = queueTime(new Row(null, 0, Day.MONDAY, false, 2, Server.US_EAST_1, Platform.STEAM, 0, MatchmakingOutcome.SUCCESS, 7, "survivor 4"), CSVParser.parse("test_data.csv"));
        System.out.println(x);
    }
}