package se.david.moviesimporter.domain;

import java.util.Objects;

import javax.persistence.Entity;
import javax.persistence.Id;

/**
 * {"id":378,"name":"prison"}
 */
@Entity
public class Keyword {
	@Id
	private long id;
	private String name;
	private boolean processed;

	public Keyword() {
	}

	public Keyword(long id, String name, boolean processed) {
		this.id = id;
		this.name = name;
		this.processed = processed;
	}

	public long getId() {
		return id;
	}

	public void setId(long id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public boolean isProcessed() {
		return processed;
	}

	public void setProcessed(boolean processed) {
		this.processed = processed;
	}

	@Override
	public boolean equals(Object o) {
		if (this == o) {
			return true;
		}
		if (o == null || getClass() != o.getClass()) {
			return false;
		}
		Keyword keyword = (Keyword) o;
		return id == keyword.id;
	}

	@Override
	public int hashCode() {
		return Objects.hash(id);
	}

	@Override
	public String toString() {
		return "Keyword{" +
				"id=" + id +
				", name='" + name + '\'' +
				'}';
	}
}
