package src;

import java.util.ArrayList;

public class TestParser {
    public static void main(String[] args) {
        ArrayList<Row> x = null;
        try {
            x = CSVParser.parse("test_data.csv");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }

        for(Row r : x) {
            System.out.println(r.queueDuration());
        }
        
    }
}
