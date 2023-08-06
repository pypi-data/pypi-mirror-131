# encoding: utf-8
"""
@author: zyl
@file: retrieval_bi_encoder.py
@time: 2021/12/16 9:45
@desc:
"""
from sentence_transformers import models

from sentence_transformers import SentenceTransformer
class Retrieval_BiEncoder:
    def __init__(self):
        """
        训练嵌入
        """
        self.model_path = "distiluse-base-multilingual-cased-v1"
        self.output_dimension = 768
        self.cuda_device = 1
        self.max_seqence_length = 128
        self.use_st_model = True
        self.train_batch_size = 16
        self.epoch = 5
        self.learning_rate = 1e-5
        self.all_scores = []
        self.best_score = 0
        self.data_top_k = 30
        self.corpus = self.get_corpus()
        save_model = "./best_model/test/",
        self.save_model = save_model
       pass

    def train(self, train_data, eval_data, loss_func='CosineSimilarityLoss',
              evaluator_func='EmbeddingSimilarityEvaluator', collection='t1', top_k=100, encode_batch_size=128):
        """

        Args:
            train_data:
            eval_data:
            save_model:
            loss_func:
            evaluator_func:
            collection:
            top_k:
            encode_batch_size:

        Returns:

        """
        model = self.get_model()

        train_obj = self.get_train_objectives(train_data, model, loss_func=loss_func)

        self.train_length = 999999999
        for t in train_obj:
            self.train_length = min(len(t[0]), self.train_length)

        print(f'train_length:{self.train_length}')

        evaluator = self.get_evaluator(dev_df, evaluator_func=evaluator_func, collection=collection, top_k=top_k,
                                       encode_batch_size=encode_batch_size)

        print(self.train_length)
        warmup_steps = math.ceil(self.train_length * 1 * 0.1)  # 10% of train data for warm-up
        evaluation_steps = math.ceil(self.train_length * 0.1)

        print('start train...')
        model.fit(train_objectives=train_obj, epochs=self.epoch, warmup_steps=warmup_steps,
                  evaluator=evaluator,
                  save_best_model=True,
                  output_path=save_model,
                  evaluation_steps=evaluation_steps,
                  callback=self.call_back,
                  optimizer_params={'lr': self.learning_rate})

        df = pd.DataFrame(self.all_scores)
        df.to_excel(save_model + 'my_score.xlsx')
        TrainRetrieval.save_parameters(self, save_model=f'{save_model}parameters.json')

    def get_model(self):
        if self.use_st_model:
            model = SentenceTransformer(self.model_path, device=f'cuda:{str(self.cuda_device)}')
        else:
            from torch import nn
            word_embedding_model = models.Transformer(self.model_path, max_seq_length=self.max_seqence_length)
            # from sentence_transformers.models.T5 import T5
            # word_embedding_model = T5(self.model_path,max_seq_length=self.max_seqence_length)
            # dense_model = models.Dense(in_features=word_embedding_model.get_word_embedding_dimension(),
            #                            out_features=word_embedding_model.get_word_embedding_dimension(),
            #                            activation_function=nn.Tanh())
            pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
                                           pooling_mode_cls_token=False,pooling_mode_max_tokens=False,
                                           pooling_mode_mean_tokens=True,pooling_mode_mean_sqrt_len_tokens=False,)
            dense_layer = models.Dense(in_features=pooling_model.get_sentence_embedding_dimension(),
                                       out_features=self.output_dimension, activation_function=nn.Tanh())
            normalize_layer = models.Normalize()
            model = SentenceTransformer(modules=[word_embedding_model, pooling_model, dense_layer, normalize_layer],
                                        device=f'cuda:{str(self.cuda_device)}')
        self.output_dimension = model.get_sentence_embedding_dimension()
        print(f'output_dimension:{self.output_dimension}')
        self.max_seqence_length = model.max_seq_length
        print(f'max_seqence_length:{self.max_seqence_length}')
        self.tokenizer = model.tokenizer
        print(f'use_pred_model: {self.model_path}')
        return model
























    @staticmethod
    def triplets_from_labeled_dataset(input_examples):
        import random
        from sentence_transformers.readers import InputExample
        # Create triplets for a [(label, sentence), (label, sentence)...] dataset
        # by using each example as an anchor and selecting randomly a
        # positive instance with the same label and a negative instance with a different label
        triplets = []
        label2sentence = defaultdict(list)
        for inp_example in input_examples:
            label2sentence[inp_example.label].append(inp_example)

        for inp_example in input_examples:
            anchor = inp_example

            if len(label2sentence[
                       inp_example.label]) < 2:  # We need at least 2 examples per label to create a triplet
                continue

            positive = None
            while positive is None or positive.guid == anchor.guid:
                positive = random.choice(label2sentence[inp_example.label])

            negative = None
            while negative is None or negative.label == anchor.label:
                negative = random.choice(input_examples)

            triplets.append(InputExample(texts=[anchor.texts[0], positive.texts[0], negative.texts[0]]))

        return triplets


    def get_train_objectives(self, train_df, model, loss_func='CosineSimilarityLoss'):
        from sentence_transformers import InputExample, SentencesDataset, losses
        from torch.utils.data import DataLoader
        from sklearn.utils import resample
        train_df = resample(train_df, replace=False)
        train_examples = []
        self.loss_func = loss_func
        if loss_func == 'MultipleNegativesRankingLoss':
            for _, sub_df in train_df.iterrows():
                if sub_df['label'] != 0:
                    train_examples.append(InputExample(texts=[sub_df['entity'], sub_df['entry']], label=1))
            train_loss = losses.MultipleNegativesRankingLoss(model=model)
        elif loss_func == 'OnlineContrastiveLoss':
            train_df = train_df[train_df['label'] != 0.0]  # type:pd.DataFrame

            dev_df = train_df.groupby('entity').apply(lambda x: x['entry'].tolist())

            scores = dev_df.index.tolist()
            eval_examples = []
            for t, r in zip(dev_df.index.tolist(), dev_df.tolist()):
                eval_examples.append(InputExample(texts=[t, r]))

            for _, sub_df in train_df.iterrows():
                if sub_df['label'] > 0:
                    label = 1
                    train_examples.append(InputExample(texts=[sub_df['entity'], sub_df['entry']], label=label))
                    train_examples.append(InputExample(texts=[sub_df['entry'], sub_df['entity']], label=label))
                else:
                    label = 0
                    train_examples.append(InputExample(texts=[sub_df['entity'], sub_df['entry']], label=label))

            train_loss = losses.OnlineContrastiveLoss(model=model)
        elif loss_func == 'multi-task':
            train_samples_MultipleNegativesRankingLoss = []
            train_samples_ConstrativeLoss = []

            for _, sub_df in train_df.iterrows():
                if sub_df['label'] > 0:
                    label = 1
                else:
                    label = 0
                train_samples_ConstrativeLoss.append(
                    InputExample(texts=[sub_df['entity'], sub_df['entry']], label=label))
                if str(label) == '1':
                    for _ in range(int(self.data_top_k / 2)):
                        train_samples_MultipleNegativesRankingLoss.append(
                            InputExample(texts=[sub_df['entity'], sub_df['entry']], label=1))
                        train_samples_MultipleNegativesRankingLoss.append(
                            InputExample(texts=[sub_df['entry'], sub_df['entity']], label=1))

            # Create data loader and loss for MultipleNegativesRankingLoss
            train_dataset_MultipleNegativesRankingLoss = SentencesDataset(
                train_samples_MultipleNegativesRankingLoss,
                model=model)
            train_dataloader_MultipleNegativesRankingLoss = DataLoader(train_dataset_MultipleNegativesRankingLoss,
                                                                       shuffle=True,
                                                                       batch_size=self.train_batch_size)
            train_loss_MultipleNegativesRankingLoss = losses.MultipleNegativesRankingLoss(model)

            # Create data loader and loss for OnlineContrastiveLoss
            train_dataset_ConstrativeLoss = SentencesDataset(train_samples_ConstrativeLoss, model=model)
            train_dataloader_ConstrativeLoss = DataLoader(train_dataset_ConstrativeLoss, shuffle=True,
                                                          batch_size=self.train_batch_size)

            # As distance metric, we use cosine distance (cosine_distance = 1-cosine_similarity)
            distance_metric = losses.SiameseDistanceMetric.COSINE_DISTANCE
            # Negative pairs should have a distance of at least 0.5
            margin = 0.5
            train_loss_ConstrativeLoss = losses.OnlineContrastiveLoss(model=model, distance_metric=distance_metric,
                                                                      margin=margin)
            train_object = [
                (train_dataloader_MultipleNegativesRankingLoss, train_loss_MultipleNegativesRankingLoss),
                (train_dataloader_ConstrativeLoss, train_loss_ConstrativeLoss)]

            return train_object

        elif loss_func == 'BatchHardSoftMarginTripletLoss':
            ### There are 4 triplet loss variants:
            ### - BatchHardTripletLoss
            ### - BatchHardSoftMarginTripletLoss
            ### - BatchSemiHardTripletLoss
            ### - BatchAllTripletLoss

            from sentence_transformers.datasets.SentenceLabelDataset import SentenceLabelDataset

            guid = 1
            self.label_map_file = "./data/v2/label_dict.xlsx"
            label_map = pd.read_excel(self.label_map_file)
            label_map = dict(zip(label_map['entry'].tolist(), label_map['label_num'].tolist()))
            train_examples = []
            for _, sub_df in train_df.iterrows():
                if sub_df['label'] != 0:
                    train_examples.append(InputExample(guid=str(guid), texts=[sub_df['entity']],
                                                       label=label_map.get(sub_df['entry'])))
                    guid += 1

            print(f'train_length:{len(train_examples)}')
            self.train_length = len(train_examples)

            train_dataset = SentenceLabelDataset(train_examples)
            train_dataloader = DataLoader(train_dataset, batch_size=self.train_batch_size, drop_last=True)
            train_loss = losses.BatchHardSoftMarginTripletLoss(model=model)
            return train_dataloader, train_loss
        else:
            for _, sub_df in train_df.iterrows():
                train_examples.append(
                    InputExample(texts=[sub_df['entity'], sub_df['entry']], label=sub_df['label']))
            train_loss = losses.CosineSimilarityLoss(model=model)

        train_dataset = SentencesDataset(train_examples, model)
        train_dataloader = DataLoader(dataset=train_dataset, shuffle=True, batch_size=self.train_batch_size)
        train_obj = [(train_dataloader, train_loss)]
        return train_obj


    def get_evaluator(self, dev_df, evaluator_func='EmbeddingSimilarityEvaluator', collection='t1',
                      top_k=100, encode_batch_size=128):
        from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
        from sklearn.utils import resample

        self.evaluator_func = evaluator_func
        dev_df = resample(dev_df, replace=False)

        if evaluator_func == 'MyEvaluator':
            from pharm_ai.panel.entry_match.revise_evaluator import MyEvaluator
            from sentence_transformers import InputExample
            dev_df = dev_df[dev_df['label'] != 0.0]  # type:pd.DataFrame
            dev_df = dev_df.groupby('entity').apply(lambda x: x['entry'].tolist())
            scores = dev_df.index.tolist()
            eval_examples = []
            for t, r in zip(dev_df.index.tolist(), dev_df.tolist()):
                eval_examples.append(InputExample(texts=[t, r]))
            evaluator = MyEvaluator.from_input_examples(eval_examples, name='sts-eval', collection=collection,
                                                        top_k=top_k, encode_batch_size=encode_batch_size)
        elif evaluator_func == 'seq_evaluator':
            from sentence_transformers import evaluation
            from sentence_transformers import InputExample
            from pharm_ai.panel.entry_match.revise_evaluator import MyEvaluator
            evaluators = []

            sentences_1 = []
            sentences_2 = []
            scores_ = []
            for _, sub_df in dev_df.iterrows():

                sentences_1.append(sub_df['entity'])
                sentences_2.append(sub_df['entry'])
                if sub_df['label'] > 0:
                    scores_.append(1)
                else:
                    scores_.append(0)

            binary_acc_evaluator = evaluation.BinaryClassificationEvaluator(sentences_1, sentences_2, scores_)
            evaluators.append(binary_acc_evaluator)

            dev_df = dev_df[dev_df['label'] != 0.0]  # type:pd.DataFrame
            dev_df = dev_df.groupby('entity').apply(lambda x: x['entry'].tolist())
            # scores = dev_df.index.tolist()
            eval_examples = []
            for t, r in zip(dev_df.index.tolist(), dev_df.tolist()):
                eval_examples.append(InputExample(texts=[t, r]))
            my_evaluator = MyEvaluator.from_input_examples(eval_examples, name='sts-eval', collection=collection,
                                                           top_k=top_k, encode_batch_size=encode_batch_size)

            evaluators.append(my_evaluator)
            seq_evaluator = evaluation.SequentialEvaluator(evaluators,
                                                           main_score_function=lambda scores: scores[-1])
            return seq_evaluator

        elif evaluator_func == 'EmbeddingSimilarityEvaluator':
            sentences_1 = []
            sentences_2 = []
            scores = []
            for _, sub_df in dev_df.iterrows():
                if sub_df['label'] != 0.0:
                    sentences_1.append(sub_df['entity'])
                    sentences_2.append(sub_df['entry'])
                    scores.append(sub_df['label'])

            evaluator = EmbeddingSimilarityEvaluator(sentences_1, sentences_2, scores)
        else:
            sentences_1 = []
            sentences_2 = []
            scores = []
            for _, sub_df in dev_df.iterrows():
                if sub_df['label'] != 0.0:
                    sentences_1.append(sub_df['entity'])
                    sentences_2.append(sub_df['entry'])
                    scores.append(sub_df['label'])
            evaluator = EmbeddingSimilarityEvaluator(sentences_1, sentences_2, scores)
        print(f'dev_length:{len(scores)}')
        self.dev_length = len(scores)
        return evaluator

    @staticmethod
    def save_parameters(para_obj, save_model='./test.json'):
        """
        存储一个对象的参数，对象参数可以是模型参数或超参数
        Args:
            para_obj: 要存储的参数的对象
            save_model: 保存路径

        Returns:

        """
        para_list = para_obj.__dir__()
        # save_para_list = ['best_score','device','max_seq_length','tokenizer']
        para = {}
        for p in para_list:
            if not p.startswith('_'):
                # if p in save_para_list:
                r = getattr(para_obj, p)
                if isinstance(r, int) or isinstance(r, str) or isinstance(r, float) or isinstance(r, list) \
                        or isinstance(r, bool):
                    para[p] = r

        with open(save_model, "w", encoding='utf-8') as f:
            # indent 超级好用，格式化保存字典，默认为None，小于0为零个空格
            # f.write(json.dumps(para,indent=4))
            json.dump(para, f, indent=4)  # 传入文件描述符，和dumps一样的结果

        para.pop("all_scores")
        with open(log_file, "a", encoding='utf-8') as f:
            json.dump(para, f, indent=4)
            f.write('\n')


    def call_back(self, score, epoch, steps):
        self.all_scores.append({str(epoch) + '-' + str(steps): score})
        if score > self.best_score:
            self.best_score = score
        print(f'epoch:{epoch}: score:{score} ')

    def get_corpus(self):
        self.corpus_file = "./data/v2/label_dict.xlsx"
        corpus = pd.read_excel(self.corpus_file)
        corpus = dict(zip(corpus['entry'].tolist(), corpus['label_num'].tolist()))
        return corpus


if __name__ == '__main__':
    pass

