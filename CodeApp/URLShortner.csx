/*
 * 
 * 
 * Functional Requirements:
    1. User submit a URL to be shortened
    2. System generates a unique short code for the URL
    3. Short code is stored in a database with the original URL
    4. User receives the short URL
    5. When the short URL is accessed, the system redirects to the original URL
    6. Support custom short codes (optional)
    7. Implement analytics to track the number of clicks on each short URL (optional)
    8. Validate the input URL to ensure it is well-formed and reachable (optional)
    9. Support encoding alorithem to generate short codes (optional)

Non-Functional Requirements:
    1. The system should be scalable to handle a large number of URLs and requests
    2. The system should have low latency for URL redirection
    3. The system should be secure to prevent unauthorized access and abuse
    4. The system should have a user-friendly interface for submitting URLs and viewing analytics (optional)

Core Entity:
    1. URL:
        - Original URL (string)
        - Short Code (string)
        - Creation Date (DateTime)
        - Click Count (int)
        - Id
        -Expiration Date (optional)

    2. RequestURL:
        - OtiginalURL (string)
        - TTLDays (int)
        - UserId (string)
        - CustomAlias (string)
    3. User:
        - UserId (string)
        - Name (string)
        - Email (string)
        - ipAddress (string)

- Encoding Startergy
- Repository:
    1. In-Memory Repository (for simplicity)
    2. Database Repository (for production use)
- Filtering strategy:
    1. Validate URL format
    2. Check if URL is reachable
    3. Check for malicious content (optional)
- URLShortenerService:
    1. CreateShortURL(RequestURL request)
    2. GetOriginalURL(string shortCode)
    3. IncrementClickCount(string shortCode)
    4. ValidateURL(string url)
    5. GenerateShortCode(string url, string customAlias = null)
 */

public interface IEncodingStrategy
{
    string Encode(string input);
}

public class Base62EncodingStrategy : IEncodingStrategy
{
    private const string Characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
    public string Encode(string input)
    {
        var hash = input.GetHashCode();
        var shortCode = new StringBuilder();
        while (hash > 0)
        {
            shortCode.Insert(0, Characters[hash % 62]);
            hash /= 62;
        }
        return shortCode.ToString();
    }
}

public class User
{
    public string UserId { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
    public string IpAddress { get; set; }
}
class URL
{
    public string OriginalURL { get; set; }
    public string ShortCode { get; set; }
    public DateTime CreationDate { get; set; }
    public int ClickCount { get; set; }
    public Guid Id { get; set; }
    public DateTime? ExpirationDate { get; set; }
}
class RequestURL
{
    public string OriginalURL { get; set; }
    public int TTLDays { get; set; }
    public string UserId { get; set; }
    public string CustomAlias { get; set; }
}
class URLRepository
{
    private readonly Dictionary<string, URL> _urlDatabase = new Dictionary<string, URL>();
    public void SaveURL(URL url)
    {
        _urlDatabase[url.ShortCode] = url;
    }
    public URL GetURL(string shortCode)
    {
        if (_urlDatabase.TryGetValue(shortCode, out var url))
        {
            return url;
        }
        throw new KeyNotFoundException("Short code not found.");
    }
}
class URLShortenerService
{
    private readonly IEncodingStrategy _encodingStrategy;
    private readonly URLRepository _repository;
    public URLShortenerService(IEncodingStrategy encodingStrategy, URLRepository repository)
    {
        _encodingStrategy = encodingStrategy;
        _repository = repository;
    }
    public string CreateShortURL(RequestURL request)
    {
        if (!Uri.IsWellFormedUriString(request.OriginalURL, UriKind.Absolute))
        {
            throw new ArgumentException("Invalid URL format.");
        }
        var shortCode = string.IsNullOrEmpty(request.CustomAlias) ? _encodingStrategy.Encode(request.OriginalURL) : request.CustomAlias;
        var url = new URL
        {
            OriginalURL = request.OriginalURL,
            ShortCode = shortCode,
            CreationDate = DateTime.UtcNow,
            ClickCount = 0,
            Id = Guid.NewGuid(),
            ExpirationDate = DateTime.UtcNow.AddDays(request.TTLDays)
        };
        _repository.SaveURL(url);
        return $"http://short.url/{shortCode}";
    }
    public string GetOriginalURL(string shortCode)
    {
        var url = _repository.GetURL(shortCode);
        if (url.ExpirationDate.HasValue && url.ExpirationDate.Value < DateTime.UtcNow)
        {
            throw new InvalidOperationException("Short URL has expired.");
        }
        url.ClickCount++;
        return url.OriginalURL;
    }
}
public interface IURLFilter
{
    bool Validate(string url);
}
class URLFormatFilter : IURLFilter
{
    public bool Validate(string url)
    {
        return Uri.IsWellFormedUriString(url, UriKind.Absolute);
    }
}

public class URLShortener
{
    private readonly IEncodingStrategy _encodingStrategy;
    private readonly Dictionary<string, string> _urlDatabase = new Dictionary<string, string>();
    public URLShortener(IEncodingStrategy encodingStrategy)
    {
        _encodingStrategy = encodingStrategy;
    }
    public string CreateShortURL(string originalUrl)
    {
        if (!Uri.IsWellFormedUriString(originalUrl, UriKind.Absolute))
        {
            throw new ArgumentException("Invalid URL format.");
        }
        var shortCode = _encodingStrategy.Encode(originalUrl);
        _urlDatabase[shortCode] = originalUrl;
        return $"http://short.url/{shortCode}";
    }
    public string GetOriginalURL(string shortCode)
    {
        if (_urlDatabase.TryGetValue(shortCode, out var originalUrl))
        {
            return originalUrl;
        }
        throw new KeyNotFoundException("Short code not found.");
    }
}