
# Document: doclaynet_document_layout_analysis.pdf



## DocLayNet: A Large Human-Annotated Dataset for Document-Layout Analysis


Birgit Pfitzmann IBM Research Rueschlikon, Switzerland bpf@zurich.ibm.com

Christoph Auer IBM Research Rueschlikon, Switzerland cau@zurich.ibm.com

Ahmed S. Nassar IBM Research

Rueschlikon, Switzerland ahn@zurich.ibm.com

Michele Dolfi IBM Research Rueschlikon, Switzerland dol@zurich.ibm.com

Peter Staar IBM Research Rueschlikon, Switzerland taa@zurich.ibm.com

Figure 1: Four examples of complex page layouts across different document categories


## KEYWORDS


PDF document conversion, layout segmentation, object-detection, data set, Machine Learning


## ACMReference Format:


Birgit Pfitzmann, Christoph Auer, Michele Dolfi, Ahmed S. Nassar, and Peter Staar. 2022. DocLayNet: A Large Human-Annotated Dataset for DocumentLayout Analysis. In Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD '22), August 14-18, 2022, Washington, DC, USA. ACM, New York, NY, USA, 9 pages. https://doi.org/10.1145/ 3534678.3539043


## ABSTRACT


Accurate document layout analysis is a key requirement for highquality PDF document conversion. With the recent availability of public, large ground-truth datasets such as PubLayNet and DocBank, deep-learning models have proven to be very effective at layout detection and segmentation. While these datasets are of adequate size to train such models, they severely lack in layout variability since they are sourced from scientific article repositories such as PubMed and arXiv only. Consequently, the accuracy of the layout segmentation drops significantly when these models are applied on more challenging and diverse layouts. In this paper, we present DocLayNet , a new, publicly available, document-layout annotation dataset in COCO format. It contains 80863 manually annotated pages from diverse data sources to represent a wide variability in layouts. For each PDF page, the layout annotations provide labelled bounding-boxes with a choice of 11 distinct classes. DocLayNet also provides a subset of double- and triple-annotated pages to determine the inter-annotator agreement. In multiple experiments, we provide baseline accuracy scores (in mAP) for a set of popular object detection models. We also demonstrate that these models fall approximately 10% behind the inter-annotator agreement. Furthermore, we provide evidence that DocLayNet is of sufficient size. Lastly, we compare models trained on PubLayNet, DocBank and DocLayNet, showing that layout predictions of the DocLayNettrained models are more robust and thus the preferred choice for general-purpose document-layout analysis.


## CCS CONCEPTS


· Informationsystems → Documentstructure ; · Appliedcomputing → Document analysis ; · Computing methodologies → Machine learning ; Computer vision ; Object detection ;

Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for third-party components of this work must be honored. For all other uses, contact the owner/author(s).

KDD '22, August 14-18, 2022, Washington, DC, USA

© 2022 Copyright held by the owner/author(s).

ACM ISBN 978-1-4503-9385-0/22/08.

https://doi.org/10.1145/3534678.3539043

KDD '22, August 14-18, 2022, Washington, DC, USA Birgit Pfitzmann, Christoph Auer, Michele Dolfi, Ahmed S. Nassar, and Peter Staar


## 1 INTRODUCTION


Despite the substantial improvements achieved with machine-learning (ML) approaches and deep neural networks in recent years, document conversion remains a challenging problem, as demonstrated by the numerous public competitions held on this topic [1-4]. The challenge originates from the huge variability in PDF documents regarding layout, language and formats (scanned, programmatic or a combination of both). Engineering a single ML model that can be applied on all types of documents and provides high-quality layout segmentation remains to this day extremely challenging [5]. To highlight the variability in document layouts, we show a few example documents from the DocLayNet dataset in Figure 1.

Akeyproblem in the process of document conversion is to understand the structure of a single document page, i.e. which segments of text should be grouped together in a unit. To train models for this task, there are currently two large datasets available to the community, PubLayNet [6] and DocBank [7]. They were introduced in 2019 and 2020 respectively and significantly accelerated the implementation of layout detection and segmentation models due to their sizes of 300K and 500K ground-truth pages. These sizes were achieved by leveraging an automation approach. The benefit of automated ground-truth generation is obvious: one can generate large ground-truth datasets at virtually no cost. However, the automation introduces a constraint on the variability in the dataset, because corresponding structured source data must be available. PubLayNet and DocBank were both generated from scientific document repositories (PubMed and arXiv), which provide XML or L A T E X sources. Those scientific documents present a limited variability in their layouts, because they are typeset in uniform templates provided by the publishers. Obviously, documents such as technical manuals, annual company reports, legal text, government tenders, etc. have very different and partially unique layouts. As a consequence, the layout predictions obtained from models trained on PubLayNet or DocBank is very reasonable when applied on scientific documents. However, for more artistic or free-style layouts, we see sub-par prediction quality from these models, which we demonstrate in Section 5.

In this paper, we present the DocLayNet dataset. It provides pageby-page layout annotation ground-truth using bounding-boxes for 11 distinct class labels on 80863 unique document pages, of which a fraction carry double- or triple-annotations. DocLayNet is similar in spirit to PubLayNet and DocBank and will likewise be made available to the public 1 in order to stimulate the document-layout analysis community. It distinguishes itself in the following aspects:

- Human Annotation : In contrast to PubLayNet and DocBank, we relied on human annotation instead of automation approaches to generate the data set.

- Large Layout Variability : We include diverse and complex layouts from a large variety of public sources.

- Detailed Label Set : We define 11 class labels to distinguish layout features in high detail. PubLayNet provides 5 labels; DocBank provides 13, although not a superset of ours.

- Redundant Annotations : A fraction of the pages in the DocLayNet data set carry more than one human annotation.

1 https://developer.ibm.com/exchanges/data/all/doclaynet

This enables experimentation with annotation uncertainty and quality control analysis.

- Pre-defined Train-, Test- & Validation-set : Like DocBank, we provide fixed train-, test- & validation-sets to ensure proportional representation of the class-labels. Further, we prevent leakage of unique layouts across sets, which has a large effect on model accuracy scores.

All aspects outlined above are detailed in Section 3. In Section 4, we will elaborate on how we designed and executed this large-scale human annotation campaign. We will also share key insights and lessons learned that might prove helpful for other parties planning to set up annotation campaigns.

In Section 5, we will present baseline accuracy numbers for a variety of object detection methods (Faster R-CNN, Mask R-CNN and YOLOv5) trained on DocLayNet. We further show how the model performance is impacted by varying the DocLayNet dataset size, reducing the label set and modifying the train/test-split. Last but not least, we compare the performance of models trained on PubLayNet, DocBank and DocLayNet and demonstrate that a model trained on DocLayNet provides overall more robust layout recovery.


## 2 RELATED WORK


While early approaches in document-layout analysis used rulebased algorithms and heuristics [8], the problem is lately addressed with deep learning methods. The most common approach is to leverage object detection models [9-15]. In the last decade, the accuracy and speed of these models has increased dramatically. Furthermore, most state-of-the-art object detection methods can be trained and applied with very little work, thanks to a standardisation effort of the ground-truth data format [16] and common deep-learning frameworks [17]. Reference data sets such as PubLayNet [6] and DocBank provide their data in the commonly accepted COCO format [16].

Lately, new types of ML models for document-layout analysis have emerged in the community [18-21]. These models do not approach the problem of layout analysis purely based on an image representation of the page, as computer vision methods do. Instead, they combine the text tokens and image representation of a page in order to obtain a segmentation. While the reported accuracies appear to be promising, a broadly accepted data format which links geometric and textual features has yet to establish.


## 3 THE DOCLAYNET DATASET


DocLayNet contains 80863 PDF pages. Among these, 7059 carry two instances of human annotations, and 1591 carry three. This amounts to 91104 total annotation instances. The annotations provide layout information in the shape of labeled, rectangular boundingboxes. We define 11 distinct labels for layout features, namely Caption , Footnote , Formula , List-item , Page-footer , Page-header , Picture , Section-header , Table , Text , and Title . Our reasoning for picking this particular label set is detailed in Section 4.

In addition to open intellectual property constraints for the source documents, we required that the documents in DocLayNet adhere to a few conditions. Firstly, we kept scanned documents

Figure 2: Distribution of DocLayNet pages across document categories.

to a minimum, since they introduce difficulties in annotation (see Section 4). As a second condition, we focussed on medium to large documents ( > 10 pages) with technical content, dense in complex tables, figures, plots and captions. Such documents carry a lot of information value, but are often hard to analyse with high accuracy due to their challenging layouts. Counterexamples of documents not included in the dataset are receipts, invoices, hand-written documents or photographs showing 'text in the wild".

The pages in DocLayNet can be grouped into six distinct categories, namely Financial Reports , Manuals , Scientific Articles , Laws & Regulations , Patents and Government Tenders . Each document category was sourced from various repositories. For example, Financial Reports contain both free-style format annual reports 2 which expose company-specific, artistic layouts as well as the more formal SEC filings. The two largest categories ( Financial Reports and Manuals ) contain a large amount of free-style layouts in order to obtain maximum variability. In the other four categories, we boosted the variability by mixing documents from independent providers, such as different government websites or publishers. In Figure 2, we show the document categories contained in DocLayNet with their respective sizes.

We did not control the document selection with regard to language. The vast majority of documents contained in DocLayNet (close to 95%) are published in English language. However, DocLayNet also contains a number of documents in other languages such as German (2.5%), French (1.0%) and Japanese (1.0%). While the document language has negligible impact on the performance of computer vision methods such as object detection and segmentation models, it might prove challenging for layout analysis methods which exploit textual features.

To ensure that future benchmarks in the document-layout analysis community can be easily compared, we have split up DocLayNet into pre-defined train-, test- and validation-sets. In this way, we can avoid spurious variations in the evaluation scores due to random splitting in train-, test- and validation-sets. We also ensured that less frequent labels are represented in train and test sets in equal proportions.

2 e.g. AAPL from https://www.annualreports.com/

Table 1 shows the overall frequency and distribution of the labels among the different sets. Importantly, we ensure that subsets are only split on full-document boundaries. This avoids that pages of the same document are spread over train, test and validation set, which can give an undesired evaluation advantage to models and lead to overestimation of their prediction accuracy. We will show the impact of this decision in Section 5.

In order to accommodate the different types of models currently in use by the community, we provide DocLayNet in an augmented COCO format [16]. This entails the standard COCO ground-truth file (in JSON format) with the associated page images (in PNG format, 1025 × 1025 pixels). Furthermore, custom fields have been added to each COCO record to specify document category, original document filename and page number. In addition, we also provide the original PDF pages, as well as sidecar files containing parsed PDF text and text-cell coordinates (in JSON). All additional files are linked to the primary page images by their matching filenames.

Despite being cost-intense and far less scalable than automation, human annotation has several benefits over automated groundtruth generation. The first and most obvious reason to leverage human annotations is the freedom to annotate any type of document without requiring a programmatic source. For most PDF documents, the original source document is not available. The latter is not a hard constraint with human annotation, but it is for automated methods. A second reason to use human annotations is that the latter usually provide a more natural interpretation of the page layout. The human-interpreted layout can significantly deviate from the programmatic layout used in typesetting. For example, 'invisible' tables might be used solely for aligning text paragraphs on columns. Such typesetting tricks might be interpreted by automated methods incorrectly as an actual table, while the human annotation will interpret it correctly as Text or other styles. The same applies to multi-line text elements, when authors decided to space them as 'invisible' list elements without bullet symbols. A third reason to gather ground-truth through human annotation is to estimate a 'natural' upper bound on the segmentation accuracy. As we will show in Section 4, certain documents featuring complex layouts can have different but equally acceptable layout interpretations. This natural upper bound for segmentation accuracy can be found by annotating the same pages multiple times by different people and evaluating the inter-annotator agreement. Such a baseline consistency evaluation is very useful to define expectations for a good target accuracy in trained deep neural network models and avoid overfitting (see Table 1). On the flip side, achieving high annotation consistency proved to be a key challenge in human annotation, as we outline in Section 4.


## 4 ANNOTATION CAMPAIGN


The annotation campaign was carried out in four phases. In phase one, we identified and prepared the data sources for annotation. In phase two, we determined the class labels and how annotations should be done on the documents in order to obtain maximum consistency. The latter was guided by a detailed requirement analysis and exhaustive experiments. In phase three, we trained the annotation staff and performed exams for quality assurance. In phase four,


### Raw Docling Table: doc_001_table_001


| class label | Count | % of Total.Train | % of Total.Test | % of Total.Val | triple inter-annotator mAP @0.5-0.95 (%).All | triple inter-annotator mAP @0.5-0.95 (%).Fin | triple inter-annotator mAP @0.5-0.95 (%).Man | triple inter-annotator mAP @0.5-0.95 (%).Sci | triple inter-annotator mAP @0.5-0.95 (%).Law | triple inter-annotator mAP @0.5-0.95 (%).Pat | triple inter-annotator mAP @0.5-0.95 (%).Ten |
|:---------------|--------:|-------------------:|------------------:|-----------------:|:-----------------------------------------------|:-----------------------------------------------|:-----------------------------------------------|:-----------------------------------------------|:-----------------------------------------------|:-----------------------------------------------|:-----------------------------------------------|
| Caption | 22524 | 2.04 | 1.77 | 2.32 | 84-89 | 40-61 | 86-92 | 94-99 | 95-99 | 69-78 | n/a |
| Footnote | 6318 | 0.6 | 0.31 | 0.58 | 83-91 | n/a | 100 | 62-88 | 85-94 | n/a | 82-97 |
| Formula | 25027 | 2.25 | 1.9 | 2.96 | 83-85 | n/a | n/a | 84-87 | 86-96 | n/a | n/a |
| List-item | 185660 | 17.19 | 13.34 | 15.82 | 87-88 | 74-83 | 90-92 | 97-97 | 81-85 | 75-88 | 93-95 |
| Page-footer | 70878 | 6.51 | 5.58 | 6 | 93-94 | 88-90 | 95-96 | 100 | 92-97 | 100 | 96-98 |
| Page-header | 58022 | 5.1 | 6.7 | 5.06 | 85-89 | 66-76 | 90-94 | 98-100 | 91-92 | 97-99 | 81-86 |
| Picture | 45976 | 4.21 | 2.78 | 5.31 | 69-71 | 56-59 | 82-86 | 69-82 | 80-95 | 66-71 | 59-76 |
| Section-header | 142884 | 12.6 | 15.77 | 12.85 | 83-84 | 76-81 | 90-92 | 94-95 | 87-94 | 69-73 | 78-86 |
| Table | 34733 | 3.2 | 2.27 | 3.6 | 77-81 | 75-80 | 83-86 | 98-99 | 58-80 | 79-84 | 70-85 |
| Text | 510377 | 45.82 | 49.28 | 45 | 84-86 | 81-86 | 88-93 | 89-93 | 87-92 | 71-79 | 87-95 |
| Title | 5071 | 0.47 | 0.3 | 0.5 | 60-72 | 24-63 | 50-63 | 94-100 | 82-96 | 68-79 | 24-56 |
| Total | 1107470 | 941123 | 99816 | 66531 | 82-83 | 71-74 | 79-81 | 89-94 | 86-91 | 71-76 | 68-85 |

Table 1: DocLayNet dataset overview. Along with the frequency of each class label, we present the relative occurrence (as % of row 'Total') in the train, test and validation sets. The inter-annotator agreement is computed as the mAP@0.5-0.95 metric between pairwise annotations from the triple-annotated pages, from which we obtain accuracy ranges.

Figure 3: Corpus Conversion Service annotation user interface. The PDF page is shown in the background, with overlaid text-cells (in darker shades). The annotation boxes can be drawn by dragging a rectangle over each segment with the respective label from the palette on the right.

we distributed the annotation workload and performed continuous quality controls. Phase one and two required a small team of experts only. For phases three and four, a group of 40 dedicated annotators were assembled and supervised.

Phase 1: Data selection and preparation. Our inclusion criteria for documents were described in Section 3. A large effort went into ensuring that all documents are free to use. The data sources include publication repositories such as arXiv 3 , government offices, company websites as well as data directory services for financial reports and patents. Scanned documents were excluded wherever possible because they can be rotated or skewed. This would not allow us to perform annotation with rectangular bounding-boxes and therefore complicate the annotation process.

Preparation work included uploading and parsing the sourced PDF documents in the Corpus Conversion Service (CCS) [22], a cloud-native platform which provides a visual annotation interface and allows for dataset inspection and analysis. The annotation interface of CCS is shown in Figure 3. The desired balance of pages between the different document categories was achieved by selective subsampling of pages with certain desired properties. For example, we made sure to include the title page of each document and bias the remaining page selection to those with figures or tables. The latter was achieved by leveraging pre-trained object detection models from PubLayNet, which helped us estimate how many figures and tables a given page contains.

Phase 2: Label selection and guideline. We reviewed the collected documents and identified the most common structural features they exhibit. This was achieved by identifying recurrent layout elements and lead us to the definition of 11 distinct class labels. These 11 class labels are Caption , Footnote , Formula , List-item , Pagefooter , Page-header , Picture , Section-header , Table , Text , and Title . Critical factors that were considered for the choice of these class labels were (1) the overall occurrence of the label, (2) the specificity of the label, (3) recognisability on a single page (i.e. no need for context from previous or next page) and (4) overall coverage of the page. Specificity ensures that the choice of label is not ambiguous, while coverage ensures that all meaningful items on a page can be annotated. We refrained from class labels that are very specific to a document category, such as Abstract in the Scientific Articles category. We also avoided class labels that are tightly linked to the semantics of the text. Labels such as Author and Affiliation , as seen in DocBank, are often only distinguishable by discriminating on

3 https://arxiv.org/

the textual content of an element, which goes beyond visual layout recognition, in particular outside the Scientific Articles category.

At first sight, the task of visual document-layout interpretation appears intuitive enough to obtain plausible annotations in most cases. However, during early trial-runs in the core team, we observed many cases in which annotators use different annotation styles, especially for documents with challenging layouts. For example, if a figure is presented with subfigures, one annotator might draw a single figure bounding-box, while another might annotate each subfigure separately. The same applies for lists, where one might annotate all list items in one block or each list item separately. In essence, we observed that challenging layouts would be annotated in different but plausible ways. To illustrate this, we show in Figure 4 multiple examples of plausible but inconsistent annotations on the same pages.

Obviously, this inconsistency in annotations is not desirable for datasets which are intended to be used for model training. To minimise these inconsistencies, we created a detailed annotation guideline. While perfect consistency across 40 annotation staff members is clearly not possible to achieve, we saw a huge improvement in annotation consistency after the introduction of our annotation guideline. A few selected, non-trivial highlights of the guideline are:

- Every list-item is an individual object instance with class label List-item . This definition is different from PubLayNet and DocBank, where all list-items are grouped together into one List object.

- A List-item is a paragraph with hanging indentation. Singleline elements can qualify as List-item if the neighbour elements expose hanging indentation. Bullet or enumeration symbols are not a requirement.

- For every Caption , there must be exactly one corresponding Picture or Table .

- Connected sub-pictures are grouped together in one Picture object.

- Formula numbers are included in a Formula object.

- Emphasised text (e.g. in italic or bold) at the beginning of a paragraph is not considered a Section-header , unless it appears exclusively on its own line.

The complete annotation guideline is over 100 pages long and a detailed description is obviously out of scope for this paper. Nevertheless, it will be made publicly available alongside with DocLayNet for future reference.

Phase 3: Training. After a first trial with a small group of people, we realised that providing the annotation guideline and a set of random practice pages did not yield the desired quality level for layout annotation. Therefore we prepared a subset of pages with two different complexity levels, each with a practice and an exam part. 974 pages were reference-annotated by one proficient core team member. Annotation staff were then given the task to annotate the same subsets (blinded from the reference). By comparing the annotations of each staff member with the reference annotations, we could quantify how closely their annotations matched the reference. Only after passing two exam levels with high annotation quality, staff were admitted into the production phase. Practice iterations

05237a14f2524e3f53c8454b074409d05078038a6a36b770fcc8ec7e540deae0

Figure 4: Examples of plausible annotation alternatives for the same page. Criteria in our annotation guideline can resolve cases A to C, while the case D remains ambiguous.

were carried out over a timeframe of 12 weeks, after which 8 of the 40 initially allocated annotators did not pass the bar.

Phase 4: Production annotation. The previously selected 80K pages were annotated with the defined 11 class labels by 32 annotators. This production phase took around three months to complete. All annotations were created online through CCS, which visualises the programmatic PDF text-cells as an overlay on the page. The page annotation are obtained by drawing rectangular bounding-boxes, as shown in Figure 3. With regard to the annotation practices, we implemented a few constraints and capabilities on the tooling level. First, we only allow non-overlapping, vertically oriented, rectangular boxes. For the large majority of documents, this constraint was sufficient and it speeds up the annotation considerably in comparison with arbitrary segmentation shapes. Second, annotator staff were not able to see each other's annotations. This was enforced by design to avoid any bias in the annotation, which could skew the numbers of the inter-annotator agreement (see Table 1). We wanted


### Raw Docling Table: doc_001_table_002


| | human. | MRCNN.R50 | MRCNN.R101 | FRCNN.R101 | YOLO.v5x6 |
|:---------------|:---------|------------:|-------------:|-------------:|------------:|
| Caption | 84-89 | 68.4 | 71.5 | 70.1 | 77.7 |
| Footnote | 83-91 | 70.9 | 71.8 | 73.7 | 77.2 |
| Formula | 83-85 | 60.1 | 63.4 | 63.5 | 66.2 |
| List-item | 87-88 | 81.2 | 80.8 | 81 | 86.2 |
| Page-footer | 93-94 | 61.6 | 59.3 | 58.9 | 61.1 |
| Page-header | 85-89 | 71.9 | 70 | 72 | 67.9 |
| Picture | 69-71 | 71.7 | 72.7 | 72 | 77.1 |
| Section-header | 83-84 | 67.6 | 69.3 | 68.4 | 74.6 |
| Table | 77-81 | 82.2 | 82.9 | 82.2 | 86.3 |
| Text | 84-86 | 84.6 | 85.8 | 85.4 | 88.1 |
| Title | 60-72 | 76.7 | 80.4 | 79.9 | 82.7 |
| All | 82-83 | 72.4 | 73.5 | 73.4 | 76.8 |

Table 2: Prediction performance (mAP@0.5-0.95) of object detection networks on DocLayNet test set. The MRCNN (Mask R-CNN) and FRCNN (Faster R-CNN) models with ResNet-50 or ResNet-101 backbone were trained based on the network architectures from the detectron2 model zoo (Mask R-CNN R50, R101-FPN 3x, Faster R-CNN R101-FPN 3x), with default configurations. The YOLO implementation utilized was YOLOv5x6 [13]. All models were initialised using pre-trained weights from the COCO 2017 dataset.

to avoid this at any cost in order to have clear, unbiased baseline numbers for human document-layout annotation. Third, we introduced the feature of snapping boxes around text segments to obtain a pixel-accurate annotation and again reduce time and effort. The CCS annotation tool automatically shrinks every user-drawn box to the minimum bounding-box around the enclosed text-cells for all purely text-based segments, which excludes only Table and Picture . For the latter, we instructed annotation staff to minimise inclusion of surrounding whitespace while including all graphical lines. A downside of snapping boxes to enclosed text cells is that some wrongly parsed PDF pages cannot be annotated correctly and need to be skipped. Fourth, we established a way to flag pages as rejected for cases where no valid annotation according to the label guidelines could be achieved. Example cases for this would be PDF pages that render incorrectly or contain layouts that are impossible to capture with non-overlapping rectangles. Such rejected pages are not contained in the final dataset. With all these measures in place, experienced annotation staff managed to annotate a single page in a typical timeframe of 20s to 60s, depending on its complexity.


## 5 EXPERIMENTS


The primary goal of DocLayNet is to obtain high-quality ML models capable of accurate document-layout analysis on a wide variety of challenging layouts. As discussed in Section 2, object detection models are currently the easiest to use, due to the standardisation of ground-truth data in COCO format [16] and the availability of general frameworks such as detectron2 [17]. Furthermore, baseline numbers in PubLayNet and DocBank were obtained using standard object detection models such as Mask R-CNN and Faster R-CNN. As such, we will relate to these object detection methods in this

Figure 5: Prediction performance (mAP@0.5-0.95) of a Mask R-CNNnetworkwithResNet50backbonetrainedonincreasing fractions of the DocLayNet dataset. The learning curve flattens around the 80% mark, indicating that increasing the size of the DocLayNet dataset with similar data will not yield significantly better predictions.

paper and leave the detailed evaluation of more recent methods mentioned in Section 2 for future work.

In this section, we will present several aspects related to the performance of object detection models on DocLayNet. Similarly as in PubLayNet, we will evaluate the quality of their predictions using mean average precision (mAP) with 10 overlaps that range from 0.5 to 0.95 in steps of 0.05 (mAP@0.5-0.95). These scores are computed by leveraging the evaluation code provided by the COCO API [16].


## Baselines for Object Detection


In Table 2, we present baseline experiments (given in mAP) on Mask R-CNN [12], Faster R-CNN [11], and YOLOv5 [13]. Both training and evaluation were performed on RGB images with dimensions of 1025 × 1025 pixels. For training, we only used one annotation in case of redundantly annotated pages. As one can observe, the variation in mAP between the models is rather low, but overall between 6 and 10% lower than the mAP computed from the pairwise human annotations on triple-annotated pages. This gives a good indication that the DocLayNet dataset poses a worthwhile challenge for the research community to close the gap between human recognition and ML approaches. It is interesting to see that Mask R-CNN and Faster R-CNN produce very comparable mAP scores, indicating that pixel-based image segmentation derived from bounding-boxes does not help to obtain better predictions. On the other hand, the more recent Yolov5x model does very well and even out-performs humans on selected labels such as Text , Table and Picture . This is not entirely surprising, as Text , Table and Picture are abundant and the most visually distinctive in a document.


### Raw Docling Table: doc_001_table_003


| Class-count | 11 | 6 | 5 | 4 |
|:---------------|-----:|:--------|:--------|:--------|
| Caption | 68 | Text | Text | Text |
| Footnote | 71 | Text | Text | Text |
| Formula | 60 | Text | Text | Text |
| List-item | 81 | Text | 82 | Text |
| Page-footer | 62 | 62 | - | - |
| Page-header | 72 | 68 | - | - |
| Picture | 72 | 72 | 72 | 72 |
| Section-header | 68 | 67 | 69 | 68 |
| Table | 82 | 83 | 82 | 82 |
| Text | 85 | 84 | 84 | 84 |
| Title | 77 | Sec.-h. | Sec.-h. | Sec.-h. |
| Overall | 72 | 73 | 78 | 77 |

Table 3: Performance of a Mask R-CNN R50 network in mAP@0.5-0.95 scores trained on DocLayNet with different class label sets. The reduced label sets were obtained by either down-mapping or dropping labels.


## Learning Curve


One of the fundamental questions related to any dataset is if it is 'large enough'. To answer this question for DocLayNet, we performed a data ablation study in which we evaluated a Mask R-CNN model trained on increasing fractions of the DocLayNet dataset. As can be seen in Figure 5, the mAP score rises sharply in the beginning and eventually levels out. To estimate the error-bar on the metrics, we ran the training five times on the entire data-set. This resulted in a 1% error-bar, depicted by the shaded area in Figure 5. In the inset of Figure 5, we show the exact same data-points, but with a logarithmic scale on the x-axis. As is expected, the mAP score increases linearly as a function of the data-size in the inset. The curve ultimately flattens out between the 80% and 100% mark, with the 80% mark falling within the error-bars of the 100% mark. This provides a good indication that the model would not improve significantly by yet increasing the data size. Rather, it would probably benefit more from improved data consistency (as discussed in Section 3), data augmentation methods [23], or the addition of more document categories and styles.


## Impact of Class Labels


The choice and number of labels can have a significant effect on the overall model performance. Since PubLayNet, DocBank and DocLayNet all have different label sets, it is of particular interest to understand and quantify this influence of the label set on the model performance. We investigate this by either down-mapping labels into more common ones (e.g. Caption → Text ) or excluding them from the annotations entirely. Furthermore, it must be stressed that all mappings and exclusions were performed on the data before model training. In Table 3, we present the mAP scores for a Mask R-CNN R50 network on different label sets. Where a label is down-mapped, we show its corresponding label, otherwise it was excluded. We present three different label sets, with 6, 5 and 4 different labels respectively. The set of 5 labels contains the same labels as PubLayNet. However, due to the different definition of


### Raw Docling Table: doc_001_table_004


| Class-count Split. | 11.Doc | 11.Page | 5.Doc | 5.Page |
|:---------------------|---------:|----------:|:--------|:---------|
| Caption | 68 | 83 | | |
| Footnote | 71 | 84 | | |
| Formula | 60 | 66 | | |
| List-item | 81 | 88 | 82 | 88 |
| Page-footer | 62 | 89 | | |
| Page-header | 72 | 90 | | |
| Picture | 72 | 82 | 72 | 82 |
| Section-header | 68 | 83 | 69 | 83 |
| Table | 82 | 89 | 82 | 90 |
| Text | 85 | 91 | 84 | 90 |
| Title | 77 | 81 | | |
| All | 72 | 84 | 78 | 87 |

Table 4: Performance of a Mask R-CNN R50 network with document-wise and page-wise split for different label sets. Naive page-wise split will result in /tildelow 10% point improvement.

lists in PubLayNet (grouped list-items) versus DocLayNet (separate list-items), the label set of size 4 is the closest to PubLayNet, in the assumption that the List is down-mapped to Text in PubLayNet. The results in Table 3 show that the prediction accuracy on the remaining class labels does not change significantly when other classes are merged into them. The overall macro-average improves by around 5%, in particular when Page-footer and Page-header are excluded.


## Impact of Document Split in Train and Test Set


Many documents in DocLayNet have a unique styling. In order to avoid overfitting on a particular style, we have split the train-, test- and validation-sets of DocLayNet on document boundaries, i.e. every document contributes pages to only one set. To the best of our knowledge, this was not considered in PubLayNet or DocBank. To quantify how this affects model performance, we trained and evaluated a Mask R-CNN R50 model on a modified dataset version. Here, the train-, test- and validation-sets were obtained by a randomised draw over the individual pages. As can be seen in Table 4, the difference in model performance is surprisingly large: pagewise splitting gains ˜ 10% in mAP over the document-wise splitting. Thus, random page-wise splitting of DocLayNet can easily lead to accidental overestimation of model performance and should be avoided.


## Dataset Comparison


Throughout this paper, we claim that DocLayNet's wider variety of document layouts leads to more robust layout detection models. In Table 5, we provide evidence for that. We trained models on each of the available datasets (PubLayNet, DocBank and DocLayNet) and evaluated them on the test sets of the other datasets. Due to the different label sets and annotation styles, a direct comparison is not possible. Hence, we focussed on the common labels among the datasets. Between PubLayNet and DocLayNet, these are Picture ,

KDD '22, August 14-18, 2022, Washington, DC, USA Birgit Pfitzmann, Christoph Auer, Michele Dolfi, Ahmed S. Nassar, and Peter Staar

Table 5: Prediction Performance (mAP@0.5-0.95) of a Mask R-CNN R50 network across the PubLayNet, DocBank & DocLayNet data-sets. By evaluating on common label classes of each dataset, we observe that the DocLayNet-trained model has much less pronounced variations in performance across all datasets.


### Raw Docling Table: doc_001_table_005


| Training on | labels | Testing on.PLN | Testing on.DB | Testing on.DLN |
|:----------------|:-----------|-----------------:|:----------------|-----------------:|
| PubLayNet (PLN) | Figure | 96 | 43 | 23 |
| PubLayNet (PLN) | Sec-header | 87 | - | 32 |
| | Table | 95 | 24 | 49 |
| | Text | 96 | - | 42 |
| | total | 93 | 34 | 30 |
| DocBank (DB) | Figure | 77 | 71 | 31 |
| DocBank (DB) | Table | 19 | 65 | 22 |
| DocBank (DB) | total | 48 | 68 | 27 |
| DocLayNet (DLN) | Figure | 67 | 51 | 72 |
| DocLayNet (DLN) | Sec-header | 53 | - | 68 |
| | Table | 87 | 43 | 82 |
| | Text | 77 | - | 84 |
| | total | 59 | 47 | 78 |

Section-header , Table and Text . Before training, we either mapped or excluded DocLayNet's other labels as specified in table 3, and also PubLayNet's List to Text . Note that the different clustering of lists (by list-element vs. whole list objects) naturally decreases the mAP score for Text .

For comparison of DocBank with DocLayNet, we trained only on Picture and Table clusters of each dataset. We had to exclude Text because successive paragraphs are often grouped together into a single object in DocBank. This paragraph grouping is incompatible with the individual paragraphs of DocLayNet. As can be seen in Table 5, DocLayNet trained models yield better performance compared to the previous datasets. It is noteworthy that the models trained on PubLayNet and DocBank perform very well on their own test set, but have a much lower performance on the foreign datasets. While this also applies to DocLayNet, the difference is far less pronounced. Thus we conclude that DocLayNet trained models are overall more robust and will produce better results for challenging, unseen layouts.


## Example Predictions


To conclude this section, we illustrate the quality of layout predictions one can expect from DocLayNet-trained models by providing a selection of examples without any further post-processing applied. Figure 6 shows selected layout predictions on pages from the test-set of DocLayNet. Results look decent in general across document categories, however one can also observe mistakes such as overlapping clusters of different classes, or entirely missing boxes due to low confidence.


## 6 CONCLUSION


In this paper, we presented the DocLayNet dataset. It provides the document conversion and layout analysis research community a new and challenging dataset to improve and fine-tune novel ML methods on. In contrast to many other datasets, DocLayNet was created by human annotation in order to obtain reliable layout ground-truth on a wide variety of publication- and typesettingstyles. Including a large proportion of documents outside the scientific publishing domain adds significant value in this respect.

From the dataset, we have derived on the one hand reference metrics for human performance on document-layout annotation (through double and triple annotations) and on the other hand evaluated the baseline performance of commonly used object detection methods. We also illustrated the impact of various dataset-related aspects on model performance through data-ablation experiments, both from a size and class-label perspective. Last but not least, we compared the accuracy of models trained on other public datasets and showed that DocLayNet trained models are more robust.

To date, there is still a significant gap between human and ML accuracy on the layout interpretation task, and we hope that this work will inspire the research community to close that gap.


## REFERENCES


- Max Göbel, Tamir Hassan, Ermelinda Oro, and Giorgio Orsi. Icdar 2013 table competition. In 2013 12th International Conference on Document Analysis and Recognition , pages 1449-1453, 2013.

- Christian Clausner, Apostolos Antonacopoulos, and Stefan Pletschacher. Icdar2017 competition on recognition of documents with complex layouts rdcl2017. In 2017 14th IAPR International Conference on Document Analysis and Recognition (ICDAR) , volume 01, pages 1404-1410, 2017.

- Hervé Déjean, Jean-Luc Meunier, Liangcai Gao, Yilun Huang, Yu Fang, Florian Kleber, and Eva-Maria Lang. ICDAR 2019 Competition on Table Detection and Recognition (cTDaR), April 2019. http://sac.founderit.com/.

- Antonio Jimeno Yepes, Peter Zhong, and Douglas Burdick. Competition on scientific literature parsing. In Proceedings of the International Conference on Document Analysis and Recognition , ICDAR, pages 605-617. LNCS 12824, SpringerVerlag, sep 2021.

- Logan Markewich, Hao Zhang, Yubin Xing, Navid Lambert-Shirzad, Jiang Zhexin, Roy Lee, Zhi Li, and Seok-Bum Ko. Segmentation for document layout analysis: not dead yet. International Journal on Document Analysis and Recognition (IJDAR) , pages 1-11, 01 2022.

- Xu Zhong, Jianbin Tang, and Antonio Jimeno-Yepes. Publaynet: Largest dataset ever for document layout analysis. In Proceedings of the International Conference on Document Analysis and Recognition , ICDAR, pages 1015-1022, sep 2019.

- Minghao Li, Yiheng Xu, Lei Cui, Shaohan Huang, Furu Wei, Zhoujun Li, and Ming Zhou. Docbank: A benchmark dataset for document layout analysis. In Proceedings of the 28th International Conference on Computational Linguistics , COLING, pages 949-960. International Committee on Computational Linguistics, dec 2020.

- Riaz Ahmad, Muhammad Tanvir Afzal, and M. Qadir. Information extraction from pdf sources based on rule-based system using integrated formats. In SemWebEval@ESWC , 2016.

- Ross B. Girshick, Jeff Donahue, Trevor Darrell, and Jitendra Malik. Rich feature hierarchies for accurate object detection and semantic segmentation. In IEEE Conference on Computer Vision and Pattern Recognition , CVPR, pages 580-587. IEEE Computer Society, jun 2014.

- Ross B. Girshick. Fast R-CNN. In 2015 IEEE International Conference on Computer Vision , ICCV, pages 1440-1448. IEEE Computer Society, dec 2015.

- Shaoqing Ren, Kaiming He, Ross Girshick, and Jian Sun. Faster r-cnn: Towards real-time object detection with region proposal networks. IEEE Transactions on Pattern Analysis and Machine Intelligence , 39(6):1137-1149, 2017.

- Kaiming He, Georgia Gkioxari, Piotr Dollár, and Ross B. Girshick. Mask R-CNN. In IEEE International Conference on Computer Vision , ICCV, pages 2980-2988. IEEE Computer Society, Oct 2017.

- Glenn Jocher, Alex Stoken, Ayush Chaurasia, Jirka Borovec, NanoCode012, TaoXie, Yonghye Kwon, Kalen Michael, Liu Changyu, Jiacong Fang, Abhiram V, Laughing, tkianai, yxNONG, Piotr Skalski, Adam Hogan, Jebastin Nadar, imyhxy, Lorenzo Mammana, Alex Wang, Cristi Fati, Diego Montes, Jan Hajek, Laurentiu

Figure 6: Example layout predictions on selected pages from the DocLayNet test-set. (A, D) exhibit favourable results on coloured backgrounds. (B, C) show accurate list-item and paragraph differentiation despite densely-spaced lines. (E) demonstrates good table and figure distinction. (F) shows predictions on a Chinese patent with multiple overlaps, label confusion and missing boxes.

Diaconu, Mai Thanh Minh, Marc, albinxavi, fatih, oleg, and wanghao yang. ultralytics/yolov5: v6.0 - yolov5n nano models, roboflow integration, tensorflow export, opencv dnn support, October 2021.

- Nicolas Carion, Francisco Massa, Gabriel Synnaeve, Nicolas Usunier, Alexander Kirillov, and Sergey Zagoruyko. End-to-end object detection with transformers. CoRR , abs/2005.12872, 2020.

- Mingxing Tan, Ruoming Pang, and Quoc V. Le. Efficientdet: Scalable and efficient object detection. CoRR , abs/1911.09070, 2019.

- Tsung-Yi Lin, Michael Maire, Serge J. Belongie, Lubomir D. Bourdev, Ross B. Girshick, James Hays, Pietro Perona, Deva Ramanan, Piotr Dollár, and C. Lawrence Zitnick. Microsoft COCO: common objects in context, 2014.

- Yuxin Wu, Alexander Kirillov, Francisco Massa, Wan-Yen Lo, and Ross Girshick. Detectron2, 2019.

- Nikolaos Livathinos, Cesar Berrospi, Maksym Lysak, Viktor Kuropiatnyk, Ahmed Nassar, Andre Carvalho, Michele Dolfi, Christoph Auer, Kasper Dinkla, and Peter W. J. Staar. Robust pdf document conversion using recurrent neural networks. In Proceedings of the 35th Conference on Artificial Intelligence , AAAI, pages 1513715145, feb 2021.

- Yiheng Xu, Minghao Li, Lei Cui, Shaohan Huang, Furu Wei, and Ming Zhou. Layoutlm: Pre-training of text and layout for document image understanding. In Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining , KDD, pages 1192-1200, New York, USA, 2020. Association for Computing Machinery.

- Shoubin Li, Xuyan Ma, Shuaiqun Pan, Jun Hu, Lin Shi, and Qing Wang. Vtlayout: Fusion of visual and text features for document layout analysis, 2021.

- Peng Zhang, Can Li, Liang Qiao, Zhanzhan Cheng, Shiliang Pu, Yi Niu, and Fei Wu. Vsr: A unified framework for document layout analysis combining vision, semantics and relations, 2021.

- Peter W J Staar, Michele Dolfi, Christoph Auer, and Costas Bekas. Corpus conversion service: A machine learning platform to ingest documents at scale. In Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining , KDD, pages 774-782. ACM, 2018.

- Connor Shorten and Taghi M. Khoshgoftaar. A survey on image data augmentation for deep learning. Journal of Big Data , 6(1):60, 2019.


# Document: rag_knowledge_intensive_nlp_tasks.pdf



## Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks


Patrick Lewis †‡ , Ethan Perez glyph[star] ,

Aleksandra Piktus † , Fabio Petroni † , Vladimir Karpukhin † , Naman Goyal † , Heinrich Küttler † ,

Mike Lewis † , Wen-tau Yih † , Tim Rocktäschel †‡ , Sebastian Riedel †‡ , Douwe Kiela †

† Facebook AI Research; ‡ University College London; glyph[star] New York University; plewis@fb.com


## Abstract


Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pretrained models with a differentiable access mechanism to explicit non-parametric memory have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) - models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, and another which can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledgeintensive NLP tasks and set the state of the art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.


## 1 Introduction


Pre-trained neural language models have been shown to learn a substantial amount of in-depth knowledge from data [47]. They can do so without any access to an external memory, as a parameterized implicit knowledge base [51, 52]. While this development is exciting, such models do have downsides: They cannot easily expand or revise their memory, can't straightforwardly provide insight into their predictions, and may produce 'hallucinations' [38]. Hybrid models that combine parametric memory with non-parametric (i.e., retrieval-based) memories [20, 26, 48] can address some of these issues because knowledge can be directly revised and expanded, and accessed knowledge can be inspected and interpreted. REALM [20] and ORQA [31], two recently introduced models that combine masked language models [8] with a differentiable retriever, have shown promising results,

Figure 1: Overview of our approach. We combine a pre-trained retriever ( Query Encoder + Document Index ) with a pre-trained seq2seq model ( Generator ) and fine-tune end-to-end. For query x , we use Maximum Inner Product Search (MIPS) to find the top-K documents z i . For final prediction y , we treat z as a latent variable and marginalize over seq2seq predictions given different documents.

but have only explored open-domain extractive question answering. Here, we bring hybrid parametric and non-parametric memory to the 'workhorse of NLP,' i.e. sequence-to-sequence (seq2seq) models.

We endow pre-trained, parametric-memory generation models with a non-parametric memory through a general-purpose fine-tuning approach which we refer to as retrieval-augmented generation (RAG). We build RAG models where the parametric memory is a pre-trained seq2seq transformer, and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We combine these components in a probabilistic model trained end-to-end (Fig. 1). The retriever (Dense Passage Retriever [26], henceforth DPR) provides latent documents conditioned on the input, and the seq2seq model (BART [32]) then conditions on these latent documents together with the input to generate the output. We marginalize the latent documents with a top-K approximation, either on a per-output basis (assuming the same document is responsible for all tokens) or a per-token basis (where different documents are responsible for different tokens). Like T5 [51] or BART, RAG can be fine-tuned on any seq2seq task, whereby both the generator and retriever are jointly learned.

There has been extensive previous work proposing architectures to enrich systems with non-parametric memory which are trained from scratch for specific tasks, e.g. memory networks [64, 55], stackaugmented networks [25] and memory layers [30]. In contrast, we explore a setting where both parametric and non-parametric memory components are pre-trained and pre-loaded with extensive knowledge. Crucially, by using pre-trained access mechanisms, the ability to access knowledge is present without additional training.

Our results highlight the benefits of combining parametric and non-parametric memory with generation for knowledge-intensive tasks -tasks that humans could not reasonably be expected to perform without access to an external knowledge source. Our RAG models achieve state-of-the-art results on open Natural Questions [29], WebQuestions [3] and CuratedTrec [2] and strongly outperform recent approaches that use specialised pre-training objectives on TriviaQA [24]. Despite these being extractive tasks, we find that unconstrained generation outperforms previous extractive approaches. For knowledge-intensive generation, we experiment with MS-MARCO [1] and Jeopardy question generation, and we find that our models generate responses that are more factual, specific, and diverse than a BART baseline. For FEVER [56] fact verification, we achieve results within 4.3% of state-of-the-art pipeline models which use strong retrieval supervision. Finally, we demonstrate that the non-parametric memory can be replaced to update the models' knowledge as the world changes. 1


## 2 Methods


We explore RAG models, which use the input sequence x to retrieve text documents z and use them as additional context when generating the target sequence y . As shown in Figure 1, our models leverage two components: (i) a retriever p η ( z | x ) with parameters η that returns (top-K truncated) distributions over text passages given a query x and (ii) a generator p θ ( y i | x, z, y 1: i -1 ) parametrized

1 Code to run experiments with RAG has been open-sourced as part of the HuggingFace Transformers Library [66] and can be found at https://github.com/huggingface/transformers/blob/master/ examples/rag/ . An interactive demo of RAG models can be found at https://huggingface.co/rag/

by θ that generates a current token based on a context of the previous i -1 tokens y 1: i -1 , the original input x and a retrieved passage z .

To train the retriever and generator end-to-end, we treat the retrieved document as a latent variable. We propose two models that marginalize over the latent documents in different ways to produce a distribution over generated text. In one approach, RAG-Sequence , the model uses the same document to predict each target token. The second approach, RAG-Token , can predict each target token based on a different document. In the following, we formally introduce both models and then describe the p η and p θ components, as well as the training and decoding procedure.


## 2.1 Models


RAG-Sequence Model The RAG-Sequence model uses the same retrieved document to generate the complete sequence . Technically, it treats the retrieved document as a single latent variable that is marginalized to get the seq2seq probability p ( y | x ) via a top-K approximation. Concretely, the top K documents are retrieved using the retriever, and the generator produces the output sequence probability for each document, which are then marginalized,

p RAG-Sequence ( y | x ) ≈ ∑ z ∈ topk ( p ( ·| x )) p η ( z | x ) p θ ( y | x, z ) = ∑ z ∈ topk ( p ( ·| x )) p η ( z | x ) N ∏ i p θ ( y i | x, z, y 1: i -1 )

RAG-Token Model In the RAG-Token model we can draw a different latent document for each target token and marginalize accordingly. This allows the generator to choose content from several documents when producing an answer. Concretely, the top K documents are retrieved using the retriever, and then the generator produces a distribution for the next output token for each document, before marginalizing, and repeating the process with the following output token, Formally, we define:

p RAG-Token ( y | x ) ≈ N ∏ i ∑ z ∈ topk ( p ( ·| x )) p η ( z | x ) p θ ( y i | x, z, y 1: i -1 )

Finally, we note that RAG can be used for sequence classification tasks by considering the target class as a target sequence of length one, in which case RAG-Sequence and RAG-Token are equivalent.


## 2.2 Retriever: DPR


The retrieval component p η ( z | x ) is based on DPR [26]. DPR follows a bi-encoder architecture:

p η ( z | x ) ∝ exp ( d ( z ) glyph[latticetop] q ( x ) ) d ( z ) = BERT d ( z ) , q ( x ) = BERT q ( x )

where d ( z ) is a dense representation of a document produced by a BERTBASE document encoder [8], and q ( x ) a query representation produced by a query encoder , also based on BERTBASE. Calculating top-k ( p η ( ·| x )) , the list of k documents z with highest prior probability p η ( z | x ) , is a Maximum Inner Product Search (MIPS) problem, which can be approximately solved in sub-linear time [23]. We use a pre-trained bi-encoder from DPR to initialize our retriever and to build the document index. This retriever was trained to retrieve documents which contain answers to TriviaQA [24] questions and Natural Questions [29]. We refer to the document index as the non-parametric memory .


## 2.3 Generator: BART


The generator component p θ ( y i | x, z, y 1: i -1 ) could be modelled using any encoder-decoder. We use BART-large [32], a pre-trained seq2seq transformer [58] with 400M parameters. To combine the input x with the retrieved content z when generating from BART, we simply concatenate them. BART was pre-trained using a denoising objective and a variety of different noising functions. It has obtained state-of-the-art results on a diverse set of generation tasks and outperforms comparably-sized T5 models [32]. We refer to the BART generator parameters θ as the parametric memory henceforth.


## 2.4 Training


We jointly train the retriever and generator components without any direct supervision on what document should be retrieved. Given a fine-tuning training corpus of input/output pairs ( x j , y j ) , we

minimize the negative marginal log-likelihood of each target, ∑ j -log p ( y j | x j ) using stochastic gradient descent with Adam [28]. Updating the document encoder BERT d during training is costly as it requires the document index to be periodically updated as REALM does during pre-training [20]. We do not find this step necessary for strong performance, and keep the document encoder (and index) fixed, only fine-tuning the query encoder BERT q and the BART generator.


## 2.5 Decoding


At test time, RAG-Sequence and RAG-Token require different ways to approximate arg max y p ( y | x ) .

RAG-Token The RAG-Token model can be seen as a standard, autoregressive seq2seq generator with transition probability: p ′ θ ( y i | x, y 1: i -1 ) = ∑ z ∈ topk ( p ( ·| x )) p η ( z i | x ) p θ ( y i | x, z i , y 1: i -1 ) To decode, we can plug p ′ θ ( y i | x, y 1: i -1 ) into a standard beam decoder.

RAG-Sequence For RAG-Sequence, the likelihood p ( y | x ) does not break into a conventional pertoken likelihood, hence we cannot solve it with a single beam search. Instead, we run beam search for each document z , scoring each hypothesis using p θ ( y i | x, z, y 1: i -1 ) . This yields a set of hypotheses Y , some of which may not have appeared in the beams of all documents. To estimate the probability of an hypothesis y we run an additional forward pass for each document z for which y does not appear in the beam, multiply generator probability with p η ( z | x ) and then sum the probabilities across beams for the marginals. We refer to this decoding procedure as 'Thorough Decoding.' For longer output sequences, | Y | can become large, requiring many forward passes. For more efficient decoding, we can make a further approximation that p θ ( y | x, z i ) ≈ 0 where y was not generated during beam search from x, z i . This avoids the need to run additional forward passes once the candidate set Y has been generated. We refer to this decoding procedure as 'Fast Decoding.'


## 3 Experiments


We experiment with RAG in a wide range of knowledge-intensive tasks. For all experiments, we use a single Wikipedia dump for our non-parametric knowledge source. Following Lee et al. [31] and Karpukhin et al. [26], we use the December 2018 dump. Each Wikipedia article is split into disjoint 100-word chunks, to make a total of 21M documents. We use the document encoder to compute an embedding for each document, and build a single MIPS index using FAISS [23] with a Hierarchical Navigable Small World approximation for fast retrieval [37]. During training, we retrieve the top k documents for each query. We consider k ∈ { 5 , 10 } for training and set k for test time using dev data. We now discuss experimental details for each task.


## 3.1 Open-domain Question Answering


Open-domain question answering (QA) is an important real-world application and common testbed for knowledge-intensive tasks [20]. We treat questions and answers as input-output text pairs ( x, y ) and train RAG by directly minimizing the negative log-likelihood of answers. We compare RAG to the popular extractive QA paradigm [5, 7, 31, 26], where answers are extracted spans from retrieved documents, relying primarily on non-parametric knowledge. We also compare to 'Closed-Book QA' approaches [52], which, like RAG, generate answers, but which do not exploit retrieval, instead relying purely on parametric knowledge. We consider four popular open-domain QA datasets: Natural Questions (NQ) [29], TriviaQA (TQA) [24]. WebQuestions (WQ) [3] and CuratedTrec (CT) [2]. As CT and WQ are small, we follow DPR [26] by initializing CT and WQ models with our NQ RAG model. We use the same train/dev/test splits as prior work [31, 26] and report Exact Match (EM) scores. For TQA, to compare with T5 [52], we also evaluate on the TQA Wiki test set.


## 3.2 Abstractive Question Answering


RAG models can go beyond simple extractive QA and answer questions with free-form, abstractive text generation. To test RAG's natural language generation (NLG) in a knowledge-intensive setting, we use the MSMARCO NLG task v2.1 [43]. The task consists of questions, ten gold passages retrieved from a search engine for each question, and a full sentence answer annotated from the retrieved passages. We do not use the supplied passages, only the questions and answers, to treat

MSMARCO as an open-domain abstractive QA task. MSMARCO has some questions that cannot be answered in a way that matches the reference answer without access to the gold passages, such as 'What is the weather in Volcano, CA?' so performance will be lower without using gold passages. We also note that some MSMARCO questions cannot be answered using Wikipedia alone. Here, RAG can rely on parametric knowledge to generate reasonable responses.


## 3.3 Jeopardy Question Generation


To evaluate RAG's generation abilities in a non-QA setting, we study open-domain question generation. Rather than use questions from standard open-domain QA tasks, which typically consist of short, simple questions, we propose the more demanding task of generating Jeopardy questions. Jeopardy is an unusual format that consists of trying to guess an entity from a fact about that entity. For example, 'The World Cup' is the answer to the question 'In 1986 Mexico scored as the first country to host this international sports competition twice.' As Jeopardy questions are precise, factual statements, generating Jeopardy questions conditioned on their answer entities constitutes a challenging knowledge-intensive generation task.

We use the splits from SearchQA [10], with 100K train, 14K dev, and 27K test examples. As this is a new task, we train a BART model for comparison. Following [67], we evaluate using the SQuAD-tuned Q-BLEU-1 metric [42]. Q-BLEU is a variant of BLEU with a higher weight for matching entities and has higher correlation with human judgment for question generation than standard metrics. We also perform two human evaluations, one to assess generation factuality, and one for specificity. We define factuality as whether a statement can be corroborated by trusted external sources, and specificity as high mutual dependence between the input and output [33]. We follow best practice and use pairwise comparative evaluation [34]. Evaluators are shown an answer and two generated questions, one from BART and one from RAG. They are then asked to pick one of four options-quuestion A is better, question B is better, both are good, or neither is good.


## 3.4 Fact Verification


FEVER [56] requires classifying whether a natural language claim is supported or refuted by Wikipedia, or whether there is not enough information to decide. The task requires retrieving evidence from Wikipedia relating to the claim and then reasoning over this evidence to classify whether the claim is true, false, or unverifiable from Wikipedia alone. FEVER is a retrieval problem coupled with an challenging entailment reasoning task. It also provides an appropriate testbed for exploring the RAG models' ability to handle classification rather than generation. We map FEVER class labels (supports, refutes, or not enough info) to single output tokens and directly train with claim-class pairs. Crucially, unlike most other approaches to FEVER, we do not use supervision on retrieved evidence. In many real-world applications, retrieval supervision signals aren't available, and models that do not require such supervision will be applicable to a wider range of tasks. We explore two variants: the standard 3-way classification task (supports/refutes/not enough info) and the 2-way (supports/refutes) task studied in Thorne and Vlachos [57]. In both cases we report label accuracy.


## 4 Results



## 4.1 Open-domain Question Answering


Table 1 shows results for RAG along with state-of-the-art models. On all four open-domain QA tasks, RAG sets a new state of the art (only on the T5-comparable split for TQA). RAG combines the generation flexibility of the 'closed-book' (parametric only) approaches and the performance of "open-book" retrieval-based approaches. Unlike REALM and T5+SSM, RAG enjoys strong results without expensive, specialized 'salient span masking' pre-training [20]. It is worth noting that RAG's retriever is initialized using DPR's retriever, which uses retrieval supervision on Natural Questions and TriviaQA. RAG compares favourably to the DPR QA system, which uses a BERT-based 'crossencoder' to re-rank documents, along with an extractive reader. RAG demonstrates that neither a re-ranker nor extractive reader is necessary for state-of-the-art performance.

There are several advantages to generating answers even when it is possible to extract them. Documents with clues about the answer but do not contain the answer verbatim can still contribute towards a correct answer being generated, which is not possible with standard extractive approaches, leading


### Raw Docling Table: doc_002_table_001


| | Model | NQ | TQA | WQ | CT |
|:------------|:---------------|-----:|:----------------|-----:|:-----|
| Closed Book | T5-11B [52] | 34.5 | - /50.1 - /60.5 | 37.4 | - - |
| | T5-11B+SSM[52] | 36.6 | | 44.7 | |
| Open | REALM [20] | 40.4 | - / - | 40.7 | 46.8 |
| Book | DPR [26] | 41.5 | 57.9 / - | 41.1 | 50.6 |
| | RAG-Token | 44.1 | 55.2/66.1 | 45.5 | 50.0 |
| | RAG-Seq. | 44.5 | 56.8/ 68.0 | 45.2 | 52.2 |

Table 1: Open-Domain QA Test Scores. For TQA, left column uses the standard test set for OpenDomain QA, right column uses the TQA-Wiki test set. See Appendix D for further details.


### Raw Docling Table: doc_002_table_002


| Model.Model | Jeopardy.B-1 | Jeopardy.QB-1 | MSMARCO.R-L | MSMARCO.B-1 | FVR3.Label | FVR2 Acc..Label |
|:------------------|:---------------|:----------------|:--------------|:--------------|-------------:|:------------------|
| SotA | - | - | 49.8 * | 49.9 * | 76.8 | 92.2 * |
| BART | 15.1 | 19.7 | 38.2 | 41.6 | 64 | 81.1 |
| RAG-Tok. RAG-Seq. | 17.3 | 22.2 | 40.1 | 41.5 | 72.5 | 89.5 |
| | 14.7 | 21.4 | 40.8 | 44.2 | 72.5 | 89.5 |

Table 2: Generation and classification Test Scores. MS-MARCO SotA is [4], FEVER-3 is [68] and FEVER-2 is [57] *Uses gold context/evidence. Best model without gold access underlined.

to more effective marginalization over documents. Furthermore, RAG can generate correct answers even when the correct answer is not in any retrieved document, achieving 11.8% accuracy in such cases for NQ, where an extractive model would score 0%.


## 4.2 Abstractive Question Answering


As shown in Table 2, RAG-Sequence outperforms BART on Open MS-MARCO NLG by 2.6 Bleu points and 2.6 Rouge-L points. RAG approaches state-of-the-art model performance, which is impressive given that (i) those models access gold passages with specific information required to generate the reference answer , (ii) many questions are unanswerable without the gold passages, and (iii) not all questions are answerable from Wikipedia alone. Table 3 shows some generated answers from our models. Qualitatively, we find that RAG models hallucinate less and generate factually correct text more often than BART. Later, we also show that RAG generations are more diverse than BART generations (see §4.5).


## 4.3 Jeopardy Question Generation


Table 2 shows that RAG-Token performs better than RAG-Sequence on Jeopardy question generation, with both models outperforming BART on Q-BLEU-1. 4 shows human evaluation results, over 452 pairs of generations from BART and RAG-Token. Evaluators indicated that BART was more factual than RAG in only 7.1% of cases, while RAG was more factual in 42.7% of cases, and both RAG and BART were factual in a further 17% of cases, clearly demonstrating the effectiveness of RAG on the task over a state-of-the-art generation model. Evaluators also find RAG generations to be more specific by a large margin. Table 3 shows typical generations from each model.

Jeopardy questions often contain two separate pieces of information, and RAG-Token may perform best because it can generate responses that combine content from several documents. Figure 2 shows an example. When generating 'Sun', the posterior is high for document 2 which mentions 'The Sun Also Rises'. Similarly, document 1 dominates the posterior when 'A Farewell to Arms' is generated. Intriguingly, after the first token of each book is generated, the document posterior flattens. This observation suggests that the generator can complete the titles without depending on specific documents. In other words, the model's parametric knowledge is sufficient to complete the titles. We find evidence for this hypothesis by feeding the BART-only baseline with the partial decoding "The Sun . BART completes the generation "The Sun Also Rises" is a novel by this author of "The Sun Also Rises" indicating the title "The Sun Also Rises" is stored in BART's parameters. Similarly, BART will complete the partial decoding "The Sun Also Rises" is a novel by this author of "A with "The Sun Also Rises" is a novel by this author of "A Farewell to Arms" . This example shows how parametric and non-parametric memories work together -the non-parametric component helps to guide the generation, drawing out specific knowledge stored in the parametric memory.


## 4.4 Fact Verification


Table 2 shows our results on FEVER. For 3-way classification, RAG scores are within 4.3% of state-of-the-art models, which are complex pipeline systems with domain-specific architectures and substantial engineering, trained using intermediate retrieval supervision, which RAG does not require.

Figure 2: RAG-Token document posterior p ( z i | x, y i , y -i ) for each generated token for input 'Hemingway" for Jeopardy generation with 5 retrieved documents. The posterior for document 1 is high when generating 'A Farewell to Arms" and for document 2 when generating 'The Sun Also Rises".


### Raw Docling Table: doc_002_table_003


| Task | Input | Model | Generation |
|:-------------------------------|:---------------------------------|:-----------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| MS- MARCO | define middle ear | BART RAG-T RAG-S | ? The middle ear is the part of the ear between the middle ear and the nose. The middle ear is the portion of the ear internal to the eardrum. The middle ear includes the tympanic cavity and the three ossicles. |
| MS- MARCO | what currency needed in scotland | BART RAG-T RAG-S | The currency needed in Scotland is Pound sterling. Pound is the currency needed in Scotland. The currency needed in Scotland is the pound sterling. |
| Jeopardy Question Gener -ation | Washington | BART RAG-T RAG-S | ? This state has the largest number of counties in the U.S. It's the only U.S. state named for a U.S. president It's the state where you'll find Mount Rainier National Park |
| Jeopardy Question Gener -ation | The Divine Comedy | BART RAG-T RAG-S | * This epic poem by Dante is divided into 3 parts: the Inferno, the Purgatorio &the Purgatorio Dante's "Inferno" is the first part of this epic poem This 14th century work is divided into 3 sections: "Inferno", "Purgatorio" &"Paradiso" |

Table 3: Examples from generation tasks. RAG models generate more specific and factually accurate responses. '?' indicates factually incorrect responses, * indicates partially correct responses.

For 2-way classification, we compare against Thorne and Vlachos [57], who train RoBERTa [35] to classify the claim as true or false given the gold evidence sentence. RAG achieves an accuracy within 2.7% of this model, despite being supplied with only the claim and retrieving its own evidence. We also analyze whether documents retrieved by RAG correspond to documents annotated as gold evidence in FEVER. We calculate the overlap in article titles between the top k documents retrieved by RAG and gold evidence annotations. We find that the top retrieved document is from a gold article in 71% of cases, and a gold article is present in the top 10 retrieved articles in 90% of cases.


## 4.5 Additional Results


Generation Diversity Section 4.3 shows that RAG models are more factual and specific than BART for Jeopardy question generation. Following recent work on diversity-promoting decoding [33, 59, 39], we also investigate generation diversity by calculating the ratio of distinct ngrams to total ngrams generated by different models. Table 5 shows that RAG-Sequence's generations are more diverse than RAG-Token's, and both are significantly more diverse than BART without needing any diversity-promoting decoding.

Retrieval Ablations A key feature of RAG is learning to retrieve relevant information for the task. To assess the effectiveness of the retrieval mechanism, we run ablations where we freeze the retriever during training. As shown in Table 6, learned retrieval improves results for all tasks.

We compare RAG's dense retriever to a word overlap-based BM25 retriever [53]. Here, we replace RAG's retriever with a fixed BM25 system, and use BM25 retrieval scores as logits when calculating p ( z | x ) . Table 6 shows the results. For FEVER, BM25 performs best, perhaps since FEVER claims are heavily entity-centric and thus well-suited for word overlap-based retrieval. Differentiable retrieval improves results on all other tasks, especially for Open-Domain QA, where it is crucial.

Index hot-swapping An advantage of non-parametric memory models like RAG is that knowledge can be easily updated at test time. Parametric-only models like T5 or BART need further training to update their behavior as the world changes. To demonstrate, we build an index using the DrQA [5] Wikipedia dump from December 2016 and compare outputs from RAG using this index to the newer index from our main results (December 2018). We prepare a list of 82 world leaders who had changed


### Raw Docling Table: doc_002_table_004


| | Factuality | Specificity |
|:------------|:-------------|:--------------|
| BART better | 7.1% | 16.8% |
| RAG better | 42.7% | 37.4% |
| Both good | 11.7% | 11.8% |
| Both poor | 17.7% | 6.9% |
| No majority | 20.8% | 20.1% |

Table 4: Human assessments for the Jeopardy Question Generation Task.


### Raw Docling Table: doc_002_table_005


| | MSMARCO | Jeopardy QGen |
|:----------|:----------|:----------------|
| Gold | 89.6% | 90.0% |
| BART | 70.7% | 32.4% |
| RAG-Token | 77.8% | 46.8% |
| RAG-Seq. | 83.5% | 53.8% |

Table 5: Ratio of distinct to total tri-grams for generation tasks.

Table 6: Ablations on the dev set. As FEVER is a classification task, both RAG models are equivalent.


### Raw Docling Table: doc_002_table_006


| Model. | NQ. | TQA.Exact Match | WQ.Exact Match | CT. | Jeopardy-QGen.B-1 | Jeopardy-QGen.QB-1 | MSMarco.R-L | MSMarco.B-1 | FVR-3.Label Accuracy | FVR-2.Label Accuracy |
|:--------------------|------:|------------------:|-----------------:|------:|--------------------:|---------------------:|--------------:|--------------:|:-----------------------|:-----------------------|
| RAG-Token-BM25 | 29.7 | 41.5 | 32.1 | 33.1 | 17.5 | 22.3 | 55.5 | 48.4 | 75.1 | 91.6 |
| RAG-Sequence-BM25 | 31.8 | 44.1 | 36.6 | 33.8 | 11.1 | 19.5 | 56.5 | 46.9 | | |
| RAG-Token-Frozen | 37.8 | 50.1 | 37.1 | 51.1 | 16.7 | 21.7 | 55.9 | 49.4 | 72.9 | 89.4 |
| RAG-Sequence-Frozen | 41.2 | 52.1 | 41.8 | 52.6 | 11.8 | 19.6 | 56.7 | 47.3 | | |
| RAG-Token | 43.5 | 54.8 | 46.5 | 51.9 | 17.9 | 22.6 | 56.2 | 49.4 | 74.5 | 90.6 |
| RAG-Sequence | 44 | 55.8 | 44.9 | 53.4 | 15.3 | 21.5 | 57.2 | 47.5 | | |

between these dates and use a template 'Who is {position}?' (e.g. 'Who is the President of Peru?') to query our NQ RAG model with each index. RAG answers 70% correctly using the 2016 index for 2016 world leaders and 68% using the 2018 index for 2018 world leaders. Accuracy with mismatched indices is low (12% with the 2018 index and 2016 leaders, 4% with the 2016 index and 2018 leaders). This shows we can update RAG's world knowledge by simply replacing its non-parametric memory.

Effect of Retrieving more documents Models are trained with either 5 or 10 retrieved latent documents, and we do not observe significant differences in performance between them. We have the flexibility to adjust the number of retrieved documents at test time, which can affect performance and runtime. Figure 3 (left) shows that retrieving more documents at test time monotonically improves Open-domain QA results for RAG-Sequence, but performance peaks for RAG-Token at 10 retrieved documents. Figure 3 (right) shows that retrieving more documents leads to higher Rouge-L for RAG-Token at the expense of Bleu-1, but the effect is less pronounced for RAG-Sequence.


### Visual Summary: doc_002_visual_003


Type: unknown


Summary: VLM analysis failed.


Figure 3: Left: NQ performance as more documents are retrieved. Center: Retrieval recall performance in NQ. Right: MS-MARCO Bleu-1 and Rouge-L as more documents are retrieved.


## 5 Related Work


Single-Task Retrieval Prior work has shown that retrieval improves performance across a variety of NLP tasks when considered in isolation. Such tasks include open-domain question answering [5, 29], fact checking [56], fact completion [48], long-form question answering [12], Wikipedia article generation [36], dialogue [41, 65, 9, 13], translation [17], and language modeling [19, 27]. Our work unifies previous successes in incorporating retrieval into individual tasks, showing that a single retrieval-based architecture is capable of achieving strong performance across several tasks.

General-Purpose Architectures for NLP Prior work on general-purpose architectures for NLP tasks has shown great success without the use of retrieval. A single, pre-trained language model has been shown to achieve strong performance on various classification tasks in the GLUE benchmarks [60, 61] after fine-tuning [49, 8]. GPT-2 [50] later showed that a single, left-to-right, pre-trained language model could achieve strong performance across both discriminative and generative tasks. For further improvement, BART [32] and T5 [51, 52] propose a single, pre-trained encoder-decoder model that leverages bi-directional attention to achieve stronger performance on discriminative and generative tasks. Our work aims to expand the space of possible tasks with a single, unified architecture, by learning a retrieval module to augment pre-trained, generative language models.

Learned Retrieval There is significant work on learning to retrieve documents in information retrieval, more recently with pre-trained, neural language models [44, 26] similar to ours. Some work optimizes the retrieval module to aid in a specific, downstream task such as question answering, using search [46], reinforcement learning [6, 63, 62], or a latent variable approach [31, 20] as in our work. These successes leverage different retrieval-based architectures and optimization techniques to achieve strong performance on a single task, while we show that a single retrieval-based architecture can be fine-tuned for strong performance on a variety of tasks.

Memory-based Architectures Our document index can be seen as a large external memory for neural networks to attend to, analogous to memory networks [64, 55]. Concurrent work [14] learns to retrieve a trained embedding for each entity in the input, rather than to retrieve raw text as in our work. Other work improves the ability of dialog models to generate factual text by attending over fact embeddings [15, 13]. A key feature of our memory is that it is comprised of raw text rather distributed representations, which makes the memory both (i) human-readable, lending a form of interpretability to our model, and (ii) human-writable, enabling us to dynamically update the model's memory by editing the document index. This approach has also been used in knowledge-intensive dialog, where generators have been conditioned on retrieved text directly, albeit obtained via TF-IDF rather than end-to-end learnt retrieval [9].

Retrieve-and-Edit approaches Our method shares some similarities with retrieve-and-edit style approaches, where a similar training input-output pair is retrieved for a given input, and then edited to provide a final output. These approaches have proved successful in a number of domains including Machine Translation [18, 22] and Semantic Parsing [21]. Our approach does have several differences, including less of emphasis on lightly editing a retrieved item, but on aggregating content from several pieces of retrieved content, as well as learning latent retrieval, and retrieving evidence documents rather than related training pairs. This said, RAG techniques may work well in these settings, and could represent promising future work.


## 6 Discussion


In this work, we presented hybrid generation models with access to parametric and non-parametric memory. We showed that our RAG models obtain state of the art results on open-domain QA. We found that people prefer RAG's generation over purely parametric BART, finding RAG more factual and specific. We conducted an thorough investigation of the learned retrieval component, validating its effectiveness, and we illustrated how the retrieval index can be hot-swapped to update the model without requiring any retraining. In future work, it may be fruitful to investigate if the two components can be jointly pre-trained from scratch, either with a denoising objective similar to BART or some another objective. Our work opens up new research directions on how parametric and non-parametric memories interact and how to most effectively combine them, showing promise in being applied to a wide variety of NLP tasks.


## Broader Impact


This work offers several positive societal benefits over previous work: the fact that it is more strongly grounded in real factual knowledge (in this case Wikipedia) makes it 'hallucinate' less with generations that are more factual, and offers more control and interpretability. RAG could be employed in a wide variety of scenarios with direct benefit to society, for example by endowing it with a medical index and asking it open-domain questions on that topic, or by helping people be more effective at their jobs.

With these advantages also come potential downsides: Wikipedia, or any potential external knowledge source, will probably never be entirely factual and completely devoid of bias. Since RAG can be employed as a language model, similar concerns as for GPT-2 [50] are valid here, although arguably to a lesser extent, including that it might be used to generate abuse, faked or misleading content in the news or on social media; to impersonate others; or to automate the production of spam/phishing content [54]. Advanced language models may also lead to the automation of various jobs in the coming decades [16]. In order to mitigate these risks, AI systems could be employed to fight against misleading content and automated spam/phishing.


## Acknowledgments


The authors would like to thank the reviewers for their thoughtful and constructive feedback on this paper, as well as HuggingFace for their help in open-sourcing code to run RAG models. The authors would also like to thank Kyunghyun Cho and Sewon Min for productive discussions and advice. EP thanks supports from the NSF Graduate Research Fellowship. PL is supported by the FAIR PhD program.


## References


- Payal Bajaj, Daniel Campos, Nick Craswell, Li Deng, Jianfeng Gao, Xiaodong Liu, Rangan Majumder, Andrew McNamara, Bhaskar Mitra, Tri Nguyen, Mir Rosenberg, Xia Song, Alina Stoica, Saurabh Tiwary, and Tong Wang. MS MARCO: A Human Generated MAchine Reading COmprehension Dataset. arXiv:1611.09268 [cs] , November 2016. URL http: //arxiv.org/abs/1611.09268 . arXiv: 1611.09268.

- Petr Baudiš and Jan Šediv` y. Modeling of the question answering task in the yodaqa system. In International Conference of the Cross-Language Evaluation Forum for European Languages , pages 222-228. Springer, 2015. URL https://link.springer.com/chapter/10.1007% 2F978-3-319-24027-5_20 .

- Jonathan Berant, Andrew Chou, Roy Frostig, and Percy Liang. Semantic Parsing on Freebase from Question-Answer Pairs. In Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing , pages 1533-1544, Seattle, Washington, USA, October 2013. Association for Computational Linguistics. URL http://www.aclweb.org/anthology/ D13-1160 .

- Bin Bi, Chenliang Li, Chen Wu, Ming Yan, and Wei Wang. Palm: Pre-training an autoencoding&autoregressive language model for context-conditioned generation. ArXiv , abs/2004.07159, 2020. URL https://arxiv.org/abs/2004.07159 .

- Danqi Chen, Adam Fisch, Jason Weston, and Antoine Bordes. Reading Wikipedia to Answer Open-Domain Questions. In Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers) , pages 1870-1879, Vancouver, Canada, July 2017. Association for Computational Linguistics. doi: 10.18653/v1/P17-1171. URL https://www.aclweb.org/anthology/P17-1171 .

- Eunsol Choi, Daniel Hewlett, Jakob Uszkoreit, Illia Polosukhin, Alexandre Lacoste, and Jonathan Berant. Coarse-to-fine question answering for long documents. In Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers) , pages 209-220, Vancouver, Canada, July 2017. Association for Computational Linguistics. doi: 10.18653/v1/P17-1020. URL https://www.aclweb.org/anthology/P17-1020 .

- Christopher Clark and Matt Gardner. Simple and Effective Multi-Paragraph Reading Comprehension. arXiv:1710.10723 [cs] , October 2017. URL http://arxiv.org/abs/1710.10723 . arXiv: 1710.10723.

- Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. In Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers) , pages 4171-4186, Minneapolis, Minnesota, June 2019. Association for Computational Linguistics. doi: 10.18653/v1/N19-1423. URL https://www.aclweb.org/anthology/N19-1423 .

- Emily Dinan, Stephen Roller, Kurt Shuster, Angela Fan, Michael Auli, and Jason Weston. Wizard of wikipedia: Knowledge-powered conversational agents. In International Conference on Learning Representations , 2019. URL https://openreview.net/forum?id=r1l73iRqKm .

- Matthew Dunn, Levent Sagun, Mike Higgins, V. Ugur Guney, Volkan Cirik, and Kyunghyun Cho. SearchQA: A New Q&A Dataset Augmented with Context from a Search Engine. arXiv:1704.05179 [cs] , April 2017. URL http://arxiv.org/abs/1704.05179 . arXiv: 1704.05179.

- Angela Fan, Mike Lewis, and Yann Dauphin. Hierarchical neural story generation. In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers) , pages 889-898, Melbourne, Australia, July 2018. Association for Computational Linguistics. doi: 10.18653/v1/P18-1082. URL https://www.aclweb.org/anthology/ P18-1082 .

- Angela Fan, Yacine Jernite, Ethan Perez, David Grangier, Jason Weston, and Michael Auli. ELI5: Long form question answering. In Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics , pages 3558-3567, Florence, Italy, July 2019. Association for Computational Linguistics. doi: 10.18653/v1/P19-1346. URL https://www.aclweb.org/ anthology/P19-1346 .

- Angela Fan, Claire Gardent, Chloe Braud, and Antoine Bordes. Augmenting transformers with KNN-based composite memory, 2020. URL https://openreview.net/forum?id= H1gx1CNKPH .

- Thibault Févry, Livio Baldini Soares, Nicholas FitzGerald, Eunsol Choi, and Tom Kwiatkowski. Entities as experts: Sparse memory access with entity supervision. ArXiv , abs/2004.07202, 2020. URL https://arxiv.org/abs/2004.07202 .

- Marjan Ghazvininejad, Chris Brockett, Ming-Wei Chang, Bill Dolan, Jianfeng Gao, Wen tau Yih, and Michel Galley. A knowledge-grounded neural conversation model. In AAAI Conference on Artificial Intelligence , 2018. URL https://www.aaai.org/ocs/index.php/ AAAI/AAAI18/paper/view/16710 .

- Katja Grace, John Salvatier, Allan Dafoe, Baobao Zhang, and Owain Evans. When will AI exceed human performance? evidence from AI experts. CoRR , abs/1705.08807, 2017. URL http://arxiv.org/abs/1705.08807 .

- Jiatao Gu, Yong Wang, Kyunghyun Cho, and Victor O.K. Li. Search engine guided neural machine translation. In AAAI Conference on Artificial Intelligence , 2018. URL https: //www.aaai.org/ocs/index.php/AAAI/AAAI18/paper/view/17282 .

- Jiatao Gu, Yong Wang, Kyunghyun Cho, and Victor O.K. Li. Search engine guided neural machine translation. In 32nd AAAI Conference on Artificial Intelligence, AAAI 2018 , 32nd AAAI Conference on Artificial Intelligence, AAAI 2018, pages 5133-5140. AAAI press, 2018. 32nd AAAI Conference on Artificial Intelligence, AAAI 2018 ; Conference date: 02-02-2018 Through 07-02-2018.

- Kelvin Guu, Tatsunori B. Hashimoto, Yonatan Oren, and Percy Liang. Generating sentences by editing prototypes. Transactions of the Association for Computational Linguistics , 6:437-450, 2018. doi: 10.1162/tacl_a_00030. URL https://www.aclweb.org/anthology/Q18-1031 .

- Kelvin Guu, Kenton Lee, Zora Tung, Panupong Pasupat, and Ming-Wei Chang. REALM: Retrieval-augmented language model pre-training. ArXiv , abs/2002.08909, 2020. URL https: //arxiv.org/abs/2002.08909 .

- Tatsunori B Hashimoto, Kelvin Guu, Yonatan Oren, and Percy S Liang. A retrieve-and-edit framework for predicting structured outputs. In S. Bengio, H. Wallach, H. Larochelle, K. Grauman, N. Cesa-Bianchi, and R. Garnett, editors, Advances in Neural Information Processing Systems 31 , pages 1005210062. Curran Associates, Inc., 2018. URL http://papers.nips.cc/paper/ 8209-a-retrieve-and-edit-framework-for-predicting-structured-outputs. pdf .

- Nabil Hossain, Marjan Ghazvininejad, and Luke Zettlemoyer. Simple and effective retrieveedit-rerank text generation. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics , pages 2532-2538, Online, July 2020. Association for Computational Linguistics. doi: 10.18653/v1/2020.acl-main.228. URL https://www.aclweb.org/ anthology/2020.acl-main.228 .

- Jeff Johnson, Matthijs Douze, and Hervé Jégou. Billion-scale similarity search with gpus. arXiv preprint arXiv:1702.08734 , 2017. URL https://arxiv.org/abs/1702.08734 .

- Mandar Joshi, Eunsol Choi, Daniel Weld, and Luke Zettlemoyer. TriviaQA: A Large Scale Distantly Supervised Challenge Dataset for Reading Comprehension. In Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers) , pages 1601-1611, Vancouver, Canada, July 2017. Association for Computational Linguistics. doi: 10.18653/v1/P17-1147. URL https://www.aclweb.org/anthology/P17-1147 .

- Armand Joulin and Tomas Mikolov. Inferring algorithmic patterns with stackaugmented recurrent nets. In Proceedings of the 28th International Conference on Neural Information Processing Systems -Volume 1 , NIPS'15, page 190-198, Cambridge, MA, USA, 2015. MIT Press. URL https://papers.nips.cc/paper/ 5857-inferring-algorithmic-patterns-with-stack-augmented-recurrent-nets .

- Vladimir Karpukhin, Barlas Oguz, Sewon Min, Ledell Wu, Sergey Edunov, Danqi Chen, and Wen-tau Yih. Dense passage retrieval for open-domain question answering. arXiv preprint arXiv:2004.04906 , 2020. URL https://arxiv.org/abs/2004.04906 .

- Urvashi Khandelwal, Omer Levy, Dan Jurafsky, Luke Zettlemoyer, and Mike Lewis. Generalization through memorization: Nearest neighbor language models. In International Conference on Learning Representations , 2020. URL https://openreview.net/forum?id=HklBjCEKvH .

- Diederik P. Kingma and Jimmy Ba. Adam: A method for stochastic optimization. In Yoshua Bengio and Yann LeCun, editors, 3rd International Conference on Learning Representations, ICLR 2015, San Diego, CA, USA, May 7-9, 2015, Conference Track Proceedings , 2015. URL http://arxiv.org/abs/1412.6980 .

- Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris Alberti, Danielle Epstein, Illia Polosukhin, Matthew Kelcey, Jacob Devlin, Kenton Lee, Kristina N. Toutanova, Llion Jones, Ming-Wei Chang, Andrew Dai, Jakob Uszkoreit, Quoc Le, and Slav Petrov. Natural Questions: a Benchmark for Question Answering Research. Transactions of the Association of Computational Linguistics , 2019. URL https://tomkwiat.users.x20web.corp.google.com/papers/ natural-questions/main-1455-kwiatkowski.pdf .

- Guillaume Lample, Alexandre Sablayrolles, Marc' Aurelio Ranzato, Ludovic Denoyer, and Herve Jegou. Large memory layers with product keys. In H. Wallach, H. Larochelle, A. Beygelzimer, F. d' Alché-Buc, E. Fox, and R. Garnett, editors, Advances in Neural Information Processing Systems 32 , pages 8548-8559. Curran Associates, Inc., 2019. URL http: //papers.nips.cc/paper/9061-large-memory-layers-with-product-keys.pdf .

- Kenton Lee, Ming-Wei Chang, and Kristina Toutanova. Latent retrieval for weakly supervised open domain question answering. In Proceedings of the 57th Annual Meeting of the Association

for Computational Linguistics , pages 6086-6096, Florence, Italy, July 2019. Association for Computational Linguistics. doi: 10.18653/v1/P19-1612. URL https://www.aclweb.org/ anthology/P19-1612 .

- Mike Lewis, Yinhan Liu, Naman Goyal, Marjan Ghazvininejad, Abdelrahman Mohamed, Omer Levy, Veselin Stoyanov, and Luke Zettlemoyer. BART: Denoising sequence-to-sequence pre-training for natural language generation, translation, and comprehension. arXiv preprint arXiv:1910.13461 , 2019. URL https://arxiv.org/abs/1910.13461 .

- Jiwei Li, Michel Galley, Chris Brockett, Jianfeng Gao, and Bill Dolan. A diversity-promoting objective function for neural conversation models. In Proceedings of the 2016 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies , pages 110-119, San Diego, California, June 2016. Association for Computational Linguistics. doi: 10.18653/v1/N16-1014. URL https://www.aclweb.org/anthology/ N16-1014 .

- Margaret Li, Jason Weston, and Stephen Roller. Acute-eval: Improved dialogue evaluation with optimized questions and multi-turn comparisons. ArXiv , abs/1909.03087, 2019. URL https://arxiv.org/abs/1909.03087 .

- Hairong Liu, Mingbo Ma, Liang Huang, Hao Xiong, and Zhongjun He. Robust neural machine translation with joint textual and phonetic embedding. In Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics , pages 3044-3049, Florence, Italy, July 2019. Association for Computational Linguistics. doi: 10.18653/v1/P19-1291. URL https://www.aclweb.org/anthology/P19-1291 .

- Peter J. Liu*, Mohammad Saleh*, Etienne Pot, Ben Goodrich, Ryan Sepassi, Lukasz Kaiser, and Noam Shazeer. Generating wikipedia by summarizing long sequences. In International Conference on Learning Representations , 2018. URL https://openreview.net/forum? id=Hyg0vbWC-.

- Yury A. Malkov and D. A. Yashunin. Efficient and robust approximate nearest neighbor search using hierarchical navigable small world graphs. IEEE Transactions on Pattern Analysis and Machine Intelligence , 42:824-836, 2016. URL https://arxiv.org/abs/1603.09320 .

- Gary Marcus. The next decade in ai: four steps towards robust artificial intelligence. arXiv preprint arXiv:2002.06177 , 2020. URL https://arxiv.org/abs/2002.06177 .

- Luca Massarelli, Fabio Petroni, Aleksandra Piktus, Myle Ott, Tim Rocktäschel, Vassilis Plachouras, Fabrizio Silvestri, and Sebastian Riedel. How decoding strategies affect the verifiability of generated text. arXiv preprint arXiv:1911.03587 , 2019. URL https: //arxiv.org/abs/1911.03587 .

- Paulius Micikevicius, Sharan Narang, Jonah Alben, Gregory Diamos, Erich Elsen, David Garcia, Boris Ginsburg, Michael Houston, Oleksii Kuchaiev, Ganesh Venkatesh, and Hao Wu. Mixed precision training. In ICLR , 2018. URL https://openreview.net/forum?id=r1gs9JgRZ .

- Nikita Moghe, Siddhartha Arora, Suman Banerjee, and Mitesh M. Khapra. Towards exploiting background knowledge for building conversation systems. In Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing , pages 2322-2332, Brussels, Belgium, October-November 2018. Association for Computational Linguistics. doi: 10.18653/v1/D18-1255. URL https://www.aclweb.org/anthology/D18-1255 .

- Preksha Nema and Mitesh M. Khapra. Towards a better metric for evaluating question generation systems. In Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing , pages 3950-3959, Brussels, Belgium, October-November 2018. Association for Computational Linguistics. doi: 10.18653/v1/D18-1429. URL https://www.aclweb.org/ anthology/D18-1429 .

- Tri Nguyen, Mir Rosenberg, Xia Song, Jianfeng Gao, Saurabh Tiwary, Rangan Majumder, and Li Deng. MS MARCO: A human generated machine reading comprehension dataset. In Tarek Richard Besold, Antoine Bordes, Artur S. d'Avila Garcez, and Greg Wayne, editors, Proceedings of the Workshop on Cognitive Computation: Integrating neural and symbolic

approaches 2016 co-located with the 30th Annual Conference on Neural Information Processing Systems (NIPS 2016), Barcelona, Spain, December 9, 2016 , volume 1773 of CEUR Workshop Proceedings . CEUR-WS.org, 2016. URL http://ceur-ws.org/Vol-1773/CoCoNIPS_ 2016_paper9.pdf .

- Rodrigo Nogueira and Kyunghyun Cho. Passage re-ranking with BERT. arXiv preprint arXiv:1901.04085 , 2019. URL https://arxiv.org/abs/1901.04085 .

- Myle Ott, Sergey Edunov, Alexei Baevski, Angela Fan, Sam Gross, Nathan Ng, David Grangier, and Michael Auli. fairseq: A fast, extensible toolkit for sequence modeling. In Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics (Demonstrations) , pages 48-53, Minneapolis, Minnesota, June 2019. Association for Computational Linguistics. doi: 10.18653/v1/N19-4009. URL https://www.aclweb. org/anthology/N19-4009 .

- Ethan Perez, Siddharth Karamcheti, Rob Fergus, Jason Weston, Douwe Kiela, and Kyunghyun Cho. Finding generalizable evidence by learning to convince q&a models. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP) , pages 2402-2411, Hong Kong, China, November 2019. Association for Computational Linguistics. doi: 10.18653/v1/D19-1244. URL https://www.aclweb.org/anthology/D19-1244 .

- Fabio Petroni, Tim Rocktäschel, Sebastian Riedel, Patrick Lewis, Anton Bakhtin, Yuxiang Wu, and Alexander Miller. Language models as knowledge bases? In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP) , pages 2463-2473, Hong Kong, China, November 2019. Association for Computational Linguistics. doi: 10.18653/v1/ D19-1250. URL https://www.aclweb.org/anthology/D19-1250 .

- Fabio Petroni, Patrick Lewis, Aleksandra Piktus, Tim Rocktäschel, Yuxiang Wu, Alexander H. Miller, and Sebastian Riedel. How context affects language models' factual predictions. In Automated Knowledge Base Construction , 2020. URL https://openreview.net/forum? id=025X0zPfn .

- Alec Radford, Karthik Narasimhan, Tim Salimans, and Ilya Sutskever. Improving Language Understanding by Generative Pre-Training, 2018. URL https://s3-us-west-2.amazonaws.com/openai-assets/research-covers/ language-unsupervised/language_understanding_paper.pdf .

- Alec Radford, Jeff Wu, Rewon Child, David Luan, Dario Amodei, and Ilya Sutskever. Language models are unsupervised multitask learners, 2019. URL https://d4mucfpksywv.cloudfront.net/better-language-models/language_ models_are_unsupervised_multitask_learners.pdf .

- Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J. Liu. Exploring the limits of transfer learning with a unified text-to-text transformer. arXiv e-prints , 2019. URL https://arxiv.org/abs/1910.10683 .

- Adam Roberts, Colin Raffel, and Noam Shazeer. How much knowledge can you pack into the parameters of a language model? arXiv e-prints , 2020. URL https://arxiv.org/abs/ 2002.08910 .

- Stephen Robertson and Hugo Zaragoza. The probabilistic relevance framework: Bm25 and beyond. Found. Trends Inf. Retr. , 3(4):333-389, April 2009. ISSN 1554-0669. doi: 10.1561/ 1500000019. URL https://doi.org/10.1561/1500000019 .

- Irene Solaiman, Miles Brundage, Jack Clark, Amanda Askell, Ariel Herbert-Voss, Jeff Wu, Alec Radford, and Jian-Bing Wang. Release strategies and the social impacts of language models. ArXiv , abs/1908.09203, 2019.

- Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, and Rob Fergus. End-to-end memory networks. In C. Cortes, N. D. Lawrence, D. D. Lee, M. Sugiyama, and R. Garnett, editors, Advances in Neural Information Processing Systems 28 , pages 2440-2448. Curran Associates, Inc., 2015. URL http://papers.nips.cc/paper/5846-end-to-end-memory-networks.pdf .

- James Thorne, Andreas Vlachos, Christos Christodoulopoulos, and Arpit Mittal. FEVER: a large-scale dataset for fact extraction and VERification. In Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long Papers) , pages 809-819, New Orleans, Louisiana, June 2018. Association for Computational Linguistics. doi: 10.18653/v1/N18-1074. URL https://www.aclweb.org/anthology/N18-1074 .

- James H. Thorne and Andreas Vlachos. Avoiding catastrophic forgetting in mitigating model biases in sentence-pair classification with elastic weight consolidation. ArXiv , abs/2004.14366, 2020. URL https://arxiv.org/abs/2004.14366 .

- Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Ł ukasz Kaiser, and Illia Polosukhin. Attention is all you need. In I. Guyon, U. V. Luxburg, S. Bengio, H. Wallach, R. Fergus, S. Vishwanathan, and R. Garnett, editors, Advances in Neural Information Processing Systems 30 , pages 5998-6008. Curran Associates, Inc., 2017. URL http://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf .

- Ashwin Vijayakumar, Michael Cogswell, Ramprasaath Selvaraju, Qing Sun, Stefan Lee, David Crandall, and Dhruv Batra. Diverse beam search for improved description of complex scenes. AAAI Conference on Artificial Intelligence , 2018. URL https://www.aaai.org/ocs/index. php/AAAI/AAAI18/paper/view/17329 .

- Alex Wang, Amanpreet Singh, Julian Michael, Felix Hill, Omer Levy, and Samuel Bowman. GLUE: A multi-task benchmark and analysis platform for natural language understanding. In Proceedings of the 2018 EMNLP Workshop BlackboxNLP: Analyzing and Interpreting Neural Networks for NLP , pages 353-355, Brussels, Belgium, November 2018. Association for Computational Linguistics. doi: 10.18653/v1/W18-5446. URL https://www.aclweb.org/ anthology/W18-5446 .

- Alex Wang, Yada Pruksachatkun, Nikita Nangia, Amanpreet Singh, Julian Michael, Felix Hill, Omer Levy, and Samuel Bowman. SuperGLUE: A Stickier Benchmark for GeneralPurpose Language Understanding Systems. In H. Wallach, H. Larochelle, A. Beygelzimer, F. d\textquotesingle Alché-Buc, E. Fox, and R. Garnett, editors, Advances in Neural Information Processing Systems 32 , pages 3261-3275. Curran Associates, Inc., 2019. URL https:// arxiv.org/abs/1905.00537 .

- Shuohang Wang, Mo Yu, Xiaoxiao Guo, Zhiguo Wang, Tim Klinger, Wei Zhang, Shiyu Chang, Gerry Tesauro, Bowen Zhou, and Jing Jiang. R 3 : Reinforced ranker-reader for open-domain question answering. In Sheila A. McIlraith and Kilian Q. Weinberger, editors, Proceedings of the Thirty-Second AAAI Conference on Artificial Intelligence, (AAAI-18), the 30th innovative Applications of Artificial Intelligence (IAAI-18), and the 8th AAAI Symposium on Educational Advances in Artificial Intelligence (EAAI-18), New Orleans, Louisiana, USA, February 2-7, 2018 , pages 5981-5988. AAAI Press, 2018. URL https://www.aaai.org/ocs/index. php/AAAI/AAAI18/paper/view/16712 .

- Shuohang Wang, Mo Yu, Jing Jiang, Wei Zhang, Xiaoxiao Guo, Shiyu Chang, Zhiguo Wang, Tim Klinger, Gerald Tesauro, and Murray Campbell. Evidence aggregation for answer reranking in open-domain question answering. In ICLR , 2018. URL https://openreview. net/forum?id=rJl3yM-Ab .

- Jason Weston, Sumit Chopra, and Antoine Bordes. Memory networks. In Yoshua Bengio and Yann LeCun, editors, 3rd International Conference on Learning Representations, ICLR 2015, San Diego, CA, USA, May 7-9, 2015, Conference Track Proceedings , 2015. URL http://arxiv.org/abs/1410.3916 .

- Jason Weston, Emily Dinan, and Alexander Miller. Retrieve and refine: Improved sequence generation models for dialogue. In Proceedings of the 2018 EMNLP Workshop SCAI: The 2nd International Workshop on Search-Oriented Conversational AI , pages 87-92, Brussels, Belgium, October 2018. Association for Computational Linguistics. doi: 10.18653/v1/W18-5713. URL https://www.aclweb.org/anthology/W18-5713 .

- Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement Delangue, Anthony Moi, Pierric Cistac, Tim Rault, Rémi Louf, Morgan Funtowicz, Joe Davison, Sam Shleifer, Patrick von Platen, Clara Ma, Yacine Jernite, Julien Plu, Canwen Xu, Teven Le Scao, Sylvain Gugger, Mariama Drame, Quentin Lhoest, and Alexander M. Rush. Huggingface's transformers: State-of-the-art natural language processing. ArXiv , abs/1910.03771, 2019.

- Shiyue Zhang and Mohit Bansal. Addressing semantic drift in question generation for semisupervised question answering. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP) , pages 2495-2509, Hong Kong, China, November 2019. Association for Computational Linguistics. doi: 10.18653/v1/D19-1253. URL https://www.aclweb.org/anthology/D19-1253 .

- Wanjun Zhong, Jingjing Xu, Duyu Tang, Zenan Xu, Nan Duan, Ming Zhou, Jiahai Wang, and Jian Yin. Reasoning over semantic-level graph for fact checking. ArXiv , abs/1909.03745, 2019. URL https://arxiv.org/abs/1909.03745 .


## Appendices for Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks



## A Implementation Details


For Open-domain QA we report test numbers using 15 retrieved documents for RAG-Token models. For RAG-Sequence models, we report test results using 50 retrieved documents, and we use the Thorough Decoding approach since answers are generally short. We use greedy decoding for QA as we did not find beam search improved results. For Open-MSMarco and Jeopardy question generation, we report test numbers using ten retrieved documents for both RAG-Token and RAG-Sequence, and we also train a BART-large model as a baseline. We use a beam size of four, and use the Fast Decoding approach for RAG-Sequence models, as Thorough Decoding did not improve performance.


## B Human Evaluation


Figure 4: Annotation interface for human evaluation of factuality. A pop-out for detailed instructions and a worked example appear when clicking "view tool guide".

Figure 4 shows the user interface for human evaluation. To avoid any biases for screen position, which model corresponded to sentence A and sentence B was randomly selected for each example. Annotators were encouraged to research the topic using the internet, and were given detailed instructions and worked examples in a full instructions tab. We included some gold sentences in order to assess the accuracy of the annotators. Two annotators did not perform well on these examples and their annotations were removed from the results.


## C Training setup Details


We train all RAG models and BART baselines using Fairseq [45]. 2 We train with mixed precision floating point arithmetic [40], distributing training across 8, 32GB NVIDIA V100 GPUs, though training and inference can be run on one GPU. We find that doing Maximum Inner Product Search with FAISS is sufficiently fast on CPU, so we store document index vectors on CPU, requiring ∼ 100 GBof CPU memory for all of Wikipedia. After submission, We have ported our code to HuggingFace Transformers [66] 3 , which achieves equivalent performance to the previous version but is a cleaner and easier to use implementation. This version is also open-sourced. We also compress the document index using FAISS's compression tools, reducing the CPU memory requirement to 36GB. Scripts to run experiments with RAG can be found at https://github.com/huggingface/transformers/ blob/master/examples/rag/README.md and an interactive demo of a RAG model can be found at https://huggingface.co/rag/

2 https://github.com/pytorch/fairseq

3 https://github.com/huggingface/transformers


## D Further Details on Open-Domain QA


For open-domain QA, multiple answer annotations are often available for a given question. These answer annotations are exploited by extractive models during training as typically all the answer annotations are used to find matches within documents when preparing training data. For RAG, we also make use of multiple annotation examples for Natural Questions and WebQuestions by training the model with each ( q, a ) pair separately, leading to a small increase in accuracy. For TriviaQA, there are often many valid answers to a given question, some of which are not suitable training targets, such as emoji or spelling variants. For TriviaQA, we filter out answer candidates if they do not occur in top 1000 documents for the query.

CuratedTrec preprocessing The answers for CuratedTrec are given in the form of regular expressions, which has been suggested as a reason why it is unsuitable for answer-generation models [20]. To overcome this, we use a pre-processing step where we first retrieve the top 1000 documents for each query, and use the answer that most frequently matches the regex pattern as the supervision target. If no matches are found, we resort to a simple heuristic: generate all possible permutations for each regex, replacing non-deterministic symbols in the regex nested tree structure with a whitespace.

TriviaQA Evaluation setups The open-domain QA community customarily uses public development datasets as test datasets, as test data for QA datasets is often restricted and dedicated to reading compehension purposes. We report our results using the datasets splits used in DPR [26], which are consistent with common practice in Open-domain QA. For TriviaQA, this test dataset is the public TriviaQA Web Development split. Roberts et al. [52] used the TriviaQA official Wikipedia test set instead. Févry et al. [14] follow this convention in order to compare with Roberts et al. [52] (See appendix of [14]). We report results on both test sets to enable fair comparison to both approaches. We find that our performance is much higher using the official Wiki test set, rather than the more conventional open-domain test set, which we attribute to the official Wiki test set questions being simpler to answer from Wikipedia.


## E Further Details on FEVER


For FEVER classification, we follow the practice from [32], and first re-generate the claim, and then classify using the representation of the final hidden state, before finally marginalizing across documents to obtain the class probabilities. The FEVER task traditionally has two sub-tasks. The first is to classify the claim as either "Supported", "Refuted" or "Not Enough Info", which is the task we explore in the main paper. FEVER's other sub-task involves extracting sentences from Wikipedia as evidence supporting the classification prediction. As FEVER uses a different Wikipedia dump to us, directly tackling this task is not straightforward. We hope to address this in future work.


## F Null Document Probabilities


We experimented with adding "Null document" mechanism to RAG, similar to REALM [20] in order to model cases where no useful information could be retrieved for a given input. Here, if k documents were retrieved, we would additionally "retrieve" an empty document and predict a logit for the null document, before marginalizing over k +1 predictions. We explored modelling this null document logit by learning (i) a document embedding for the null document, (ii) a static learnt bias term, or (iii) a neural network to predict the logit. We did not find that these improved performance, so in the interests of simplicity, we omit them. For Open MS-MARCO, where useful retrieved documents cannot always be retrieved, we observe that the model learns to always retrieve a particular set of documents for questions that are less likely to benefit from retrieval, suggesting that null document mechanisms may not be necessary for RAG.


## G Parameters


Our RAG models contain the trainable parameters for the BERT-base query and document encoder of DPR, with 110M parameters each (although we do not train the document encoder ourselves) and 406M trainable parameters from BART-large, 406M parameters, making a total of 626M trainable


### Raw Docling Table: doc_002_table_007


| Task | Train | Development | Test |
|:-----------------------------|--------:|--------------:|:--------|
| Natural Questions | 79169 | 8758 | 3611 |
| TriviaQA | 78786 | 8838 | 11314 |
| WebQuestions | 3418 | 362 | 2033 |
| CuratedTrec | 635 | 134 | 635 |
| Jeopardy Question Generation | 97392 | 13714 | 26849 |
| MS-MARCO | 153726 | 12468 | 101093* |
| FEVER-3-way | 145450 | 10000 | 10000 |
| FEVER-2-way | 96966 | 6666 | 6666 |

Table 7: Number of instances in the datasets used. *A hidden subset of this data is used for evaluation

parameters. The best performing "closed-book" (parametric only) open-domain QA model is T5-11B with 11 Billion trainable parameters. The T5 model with the closest number of parameters to our models is T5-large (770M parameters), which achieves a score of 28.9 EM on Natural Questions [52], substantially below the 44.5 that RAG-Sequence achieves, indicating that hybrid parametric/nonparametric models require far fewer trainable parameters for strong open-domain QA performance. The non-parametric memory index does not consist of trainable parameters, but does consists of 21M 728 dimensional vectors, consisting of 15.3B values. These can be easily be stored at 8-bit floating point precision to manage memory and disk footprints.


## H Retrieval Collapse


In preliminary experiments, we observed that for some tasks such as story generation [11], the retrieval component would 'collapse' and learn to retrieve the same documents regardless of the input. In these cases, once retrieval had collapsed, the generator would learn to ignore the documents, and the RAG model would perform equivalently to BART. The collapse could be due to a less-explicit requirement for factual knowledge in some tasks, or the longer target sequences, which could result in less informative gradients for the retriever. Perez et al. [46] also found spurious retrieval results when optimizing a retrieval component in order to improve performance on downstream tasks.


## I Number of instances per dataset


The number of training, development and test datapoints in each of our datasets is shown in Table 7.