package se.david.moviesimporter.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import se.david.moviesimporter.domain.ProductionCompany;

@Repository
public interface ProductionCompanyRepository extends JpaRepository<ProductionCompany, Long> {
}
