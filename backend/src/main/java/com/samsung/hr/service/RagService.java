package com.samsung.hr.service;

import com.samsung.hr.domain.RagDocument;
import com.samsung.hr.repository.RagDocumentRepository;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.UUID;

@Service
public class RagService {

    private final RagDocumentRepository repository;
    private final TemporalInterviewService temporalService;
    private final Path uploadDir;

    public RagService(
            RagDocumentRepository repository,
            TemporalInterviewService temporalService,
            @Value("${app.rag-upload-dir}") String uploadDir) throws IOException {
        this.repository = repository;
        this.temporalService = temporalService;
        this.uploadDir = Path.of(uploadDir);
        Files.createDirectories(this.uploadDir);
    }

    @Transactional
    public RagDocument upload(MultipartFile file) throws IOException {
        if (!file.getOriginalFilename().toLowerCase().endsWith(".pdf")) {
            throw new IllegalArgumentException("Only PDF files are supported");
        }

        RagDocument doc = new RagDocument();
        doc.setFileName(file.getOriginalFilename());
        doc = repository.save(doc);

        Path dest = uploadDir.resolve(doc.getId() + ".pdf");
        file.transferTo(dest);
        doc.setStoragePath(dest.toAbsolutePath().toString());

        try {
            int chunks = temporalService.ingestRagDocument(dest.toString(), doc.getId());
            doc.setChunkCount(chunks);
            doc.setIngestStatus("READY");
        } catch (Exception e) {
            doc.setIngestStatus("FAILED");
            throw e;
        }

        return repository.save(doc);
    }

    public List<RagDocument> list() {
        return repository.findAll();
    }
}
