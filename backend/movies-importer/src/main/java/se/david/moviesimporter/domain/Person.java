package se.david.moviesimporter.domain;

import java.util.Objects;

import javax.persistence.Entity;
import javax.persistence.Id;

/*
{"adult":false,"id":1293830,"name":"Santiago  Bertolino","popularity":0.6}
 */
@Entity
public class Person {
	@Id
	private long id;
	private boolean adult;
	private String name;
	private double popularity;

	public Person() {
	}

	public Person(long id, boolean adult, String name, double popularity) {
		this.id = id;
		this.adult = adult;
		this.name = name;
		this.popularity = popularity;
	}

	public long getId() {
		return id;
	}

	public void setId(long id) {
		this.id = id;
	}

	public boolean isAdult() {
		return adult;
	}

	public void setAdult(boolean adult) {
		this.adult = adult;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public double getPopularity() {
		return popularity;
	}

	public void setPopularity(double popularity) {
		this.popularity = popularity;
	}

	@Override
	public boolean equals(Object o) {
		if (this == o) {
			return true;
		}
		if (o == null || getClass() != o.getClass()) {
			return false;
		}
		Person person = (Person) o;
		return id == person.id &&
				adult == person.adult &&
				Double.compare(person.popularity, popularity) == 0 &&
				Objects.equals(name, person.name);
	}

	@Override
	public int hashCode() {
		return Objects.hash(id, adult, name, popularity);
	}

	@Override
	public String toString() {
		return "Person{" +
				"id=" + id +
				", adult=" + adult +
				", name='" + name + '\'' +
				", popularity=" + popularity +
				'}';
	}
}
