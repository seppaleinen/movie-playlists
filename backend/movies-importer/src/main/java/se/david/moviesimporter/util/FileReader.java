package se.david.moviesimporter.util;

import static org.slf4j.LoggerFactory.getLogger;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.nio.charset.StandardCharsets;
import java.util.stream.Stream;
import java.util.zip.GZIPInputStream;

import org.slf4j.Logger;

public final class FileReader {
	private static final Logger log = getLogger(FileReader.class);

	private FileReader() {
	}

	public static Stream<String> readFile(File file) {
		try  {
			InputStream fileStream = new FileInputStream(file);
			InputStream gzipStream = new GZIPInputStream(fileStream);
			Reader decoder = new InputStreamReader(gzipStream, StandardCharsets.UTF_8.name());
			BufferedReader buffered = new BufferedReader(decoder);
			return buffered.lines();
		} catch (Exception e) {
			log.error("Error: {}", e.getMessage(), e);
			return Stream.empty();
		}
	}
}
