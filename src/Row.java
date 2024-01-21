package src;


//role: killer = true, survivor = false


public record Row (String matchID, int startTime, Day dayOfWeek, boolean killer, int partySize, Server serverName, Platform platform, long queueDuration, MatchmakingOutcome mmOutcome, int mmr, String characterName)
{
}
