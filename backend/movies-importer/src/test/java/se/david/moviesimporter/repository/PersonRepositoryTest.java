package se.david.moviesimporter.repository;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.Arrays;
import java.util.List;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.junit.jupiter.SpringExtension;

import se.david.moviesimporter.domain.Person;

@ExtendWith(SpringExtension.class)
@DataJpaTest
public class PersonRepositoryTest {
	@Autowired
	private PersonRepository personRepository;

	@Test
	public void asd() {
		Person person = new Person(1, false, "name", 0.0);
		personRepository.saveAndFlush(person);

		List<Person> result = personRepository.saveAll(Arrays.asList(person));

		assertEquals(1, result.size());
	}

	@Test
	public void asd2() {
		Person person = new Person(1, false, "name", 0.0);

		List<Person> result = personRepository.saveAll(Arrays.asList(person, person));

		assertEquals(1, personRepository.findAll().size(), personRepository.findAll().toString());
	}
	@Test
	public void asd3() {
		Person person = new Person(1, false, "name", 0.0);
		personRepository.saveAndFlush(person);
		personRepository.saveAndFlush(person);
		List<Person> result = personRepository.findAllById(Arrays.asList(person.getId()));

		assertEquals(1, result.size(), result.toString());
	}
}
