package se.david.moviesimporter.repository;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import java.util.stream.Stream;

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
		Person person = new Person(1, false, "name", 0.0, false);
		personRepository.saveAndFlush(person);

		List<Person> result = personRepository.saveAll(Arrays.asList(person));

		assertEquals(1, result.size());
	}

	@Test
	public void asd2() {
		Person person = new Person(1, false, "name", 0.0, false);

		List<Person> result = personRepository.saveAll(Arrays.asList(person, person));

		assertEquals(1, personRepository.findAll().size(), personRepository.findAll().toString());
	}
	@Test
	public void asd3() {
		Person person = new Person(1, false, "name", 0.0, false);
		personRepository.saveAndFlush(person);
		personRepository.saveAndFlush(person);
		List<Person> result = personRepository.findAllById(Arrays.asList(person.getId()));

		assertEquals(1, result.size(), result.toString());
	}

	@Test
	public void findAllUnprocessed() {
		personRepository.saveAndFlush(new Person(1, false, "name1", 0.0, false));
		personRepository.saveAndFlush(new Person(2, false, "name2", 0.0, true));

		List<Long> allUnprocessed = personRepository.findAllUnprocessed();

		assertTrue(allUnprocessed.stream().anyMatch(a -> a == 1));
		assertFalse(allUnprocessed.stream().anyMatch(a -> a == 2));
	}
}
