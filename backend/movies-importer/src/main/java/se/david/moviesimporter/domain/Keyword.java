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

	@Override
	public boolean equals(Object o) {
		if (this == o) {
			return true;
		}
		if (o == null || getClass() != o.getClass()) {
			return false;
		}
		Keyword keyword = (Keyword) o;
		return id == keyword.id &&
				Objects.equals(name, keyword.name);
	}

	@Override
	public int hashCode() {
		return Objects.hash(id, name);
	}

	@Override
	public String toString() {
		return "Keyword{" +
				"id=" + id +
				", name='" + name + '\'' +
				'}';
	}
}
