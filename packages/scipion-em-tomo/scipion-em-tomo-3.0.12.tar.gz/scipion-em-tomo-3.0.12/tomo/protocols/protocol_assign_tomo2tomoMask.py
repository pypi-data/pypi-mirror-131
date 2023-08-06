# **************************************************************************
# *
# * Authors:     Scipion Team
# *
# * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************
from os import symlink
from os.path import basename, abspath

from pyworkflow import BETA
from pyworkflow.protocol.params import PointerParam
from pyworkflow.utils import removeExt
from pwem.protocols import EMProtocol
from tomo.objects import TomoMask

MATERIALS_SUFFIX = '_materials'


class ProtAssignTomo2TomoMask(EMProtocol):
    """ This protocol assign tomograms to tomo masks (segmentations)."""

    _label = 'assign tomograms to tomo masks (segmentations)'
    _devStatus = BETA

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tomoDict = {}

    def _defineParams(self, form):
        form.addSection(label='Input')
        form.addParam('inTomoMasks', PointerParam,
                      pointerClass='SetOfTomoMasks',
                      label='Tomo masks (segmentations)',
                      help='Select the tomo masks desired to be referred to the introduced tomograms. The match '
                           'between both sets is carried out firstly by tsId and if not possible, then it will try '
                           'to do it by filename.')
        form.addParam('inputTomos', PointerParam,
                      pointerClass='SetOfTomograms',
                      label='Tomograms',
                      help='Select the tomograms to be assigned to the input tomo masks.')

    # --------------------------- INSERT steps functions --------------------------
    def _insertAllSteps(self):
        self._insertFunctionStep('createOutputStep')

    # --------------------------- STEPS functions --------------------------------------------
    def createOutputStep(self):
        inTomos = self.inputTomos.get()
        inTomoMasks = self.inTomoMasks.get()
        outputSetOfTomoMasks = inTomoMasks.create(self._getPath())
        outputSetOfTomoMasks.copyInfo(inTomoMasks)

        if self._isMatchingByTsId():
            tomoTsIds = [tomo.getTsId() for tomo in inTomos]
            for inTomoMask in inTomoMasks:
                outTomoMask = self.setMatchingTomogram(tomoTsIds, inTomoMask, inTomos)
                outputSetOfTomoMasks.append(outTomoMask)
        else:
            # Membrane Annotator tool adds suffix _materials to the generated tomomasks
            tomoBaseNames = [basename(tomo.getFileName().replace(MATERIALS_SUFFIX, '')) for tomo in inTomos]
            for inTomoMask in inTomoMasks:
                outTomoMask = self.setMatchingTomogram(tomoBaseNames, inTomoMask, inTomos, isMatchingByTsId=False)
                outputSetOfTomoMasks.append(outTomoMask)

        self._defineOutputs(outputTomoMasks=outputSetOfTomoMasks)
        self._defineSourceRelation(inTomos, outputSetOfTomoMasks)

    # --------------------------- UTILS functions --------------------------------------------
    def setMatchingTomogram(self, idList, inTomoMask, inTomos, isMatchingByTsId=True):
        inFileName = inTomoMask.getFileName()
        outFileName = self._getExtraPath(basename(inFileName))
        symlink(abspath(inFileName), abspath(outFileName))
        outTomoMask = TomoMask()
        outTomoMask.setLocation(inFileName)
        outTomoMask.copyInfo(inTomoMask)
        outTomoMask.setFileName = outFileName
        if isMatchingByTsId:
            outTomoMask.setVolName(inTomos[idList.index(inTomoMask.getTsId()) + 1].getFileName())
        else:
            outTomoMask.setVolName(inTomos[idList.index(basename(inTomoMask.getFileName().replace(
                MATERIALS_SUFFIX, ''))) + 1].getFileName())
        return outTomoMask

    def _updateItem(self, item, row):
        for tomoName in self.tomoDict:
            if removeExt(tomoName) in item.getFileName():
                item.setVolName(tomoName)
                item.setVolId(self.tomoDict.get(tomoName))
                break

    def _isMatchingByTsId(self):
        tsId = '_tsId'
        if hasattr(self.inTomoMasks.get().getFirstItem(), tsId) and \
                hasattr(self.inputTomos.get().getFirstItem(), tsId):
            if self.inTomoMasks.get().getFirstItem().getTsId() and self.inputTomos.get().getFirstItem().getTsId():
                return True
            else:
                return False
        else:
            return False

    # --------------------------- INFO functions --------------------------------------------
    def _validate(self):
        errors = []
        inTomoMasks = self.inTomoMasks.get()
        inTomos = self.inputTomos.get()
        tol = 0.01
        if abs(inTomos.getSamplingRate() - inTomoMasks.getSamplingRate() > tol):
            errors.append('Sampling rate of input sets of tomomasks and tomograms differ in more '
                          'than %.2f Å/pix.' % tol)
        else:
            # Check match by tsId
            tomoMaskTsIds = [tomoMask.getTsId() for tomoMask in inTomoMasks]
            tomoTsIds = [tomo.getTsId() for tomo in inTomos]
            numberMatchesByTsId = len(set(tomoTsIds) & set(tomoMaskTsIds))  # Length of the intersection of both lists

            # Check match by basename
            tomoMaskBaseNames = [tomoMask.getFileName().replace(MATERIALS_SUFFIX, '') for tomoMask in inTomoMasks]
            tomoBaseNames = [tomo.getFileName() for tomo in inTomos]
            numberMatchesByBaseName = len(set(tomoMaskBaseNames) & set(tomoBaseNames))  # Length of the intersection of both lists

            if numberMatchesByTsId == 0 and numberMatchesByBaseName:
                errors.append('Unable to find any match between the introduced datasets after checking the tsIds and '
                              'the basename of all elements.')
        return errors

    def _warnings(self):
        warnings = []
        inTomoMasks = self.inTomoMasks.get()
        inTomos = self.inputTomos.get()
        if self._isMatchingByTsId():
            notMatchingMsg = ''
            # Check match by tsId
            tomoTsIds = [tomo.getTsId() for tomo in inTomos]
            for tomoMask in inTomoMasks:
                if tomoMask.getTsId() not in tomoTsIds:
                    notMatchingMsg += '\n\t-%s' % tomoMask.getFileName()
            if notMatchingMsg:
                warnings.append('Not able to find a tsId-based match for the following tomomasks in '
                                'the introduced tomograms:' + notMatchingMsg)
        else:
            notMatchingMsg = ''
            # Check match by basename
            tomoBaseNames = [basename(tomo.getFileName().replace(MATERIALS_SUFFIX, '')) for tomo in inTomos]
            for tomoMask in inTomoMasks:
                tomoMaskName = tomoMask.getFileName()
                tomoMaskBaseName = basename(tomoMaskName.replace(MATERIALS_SUFFIX, ''))
                if tomoMaskBaseName not in tomoBaseNames:
                    notMatchingMsg += '\n\t-%s' % tomoMaskName
            if notMatchingMsg:
                warnings.append('Not able to find a basename-based match for the following tomomasks in '
                                'the introduced tomograms:' + notMatchingMsg)

        return warnings

    def _summary(self):
        summary = []
        if not hasattr(self, 'outputSubtomograms'):
            summary.append("Output subtomograms not ready yet.")
        else:
            summary.append("%s tomograms assigned to %s subtomograms." %
                           (self.getObjectTag('inputTomos'), self.getObjectTag('inputSubtomos')))
        return summary

    def _methods(self):
        methods = []
        if not hasattr(self, 'outputSubtomograms'):
            methods.append("Output subtomograms not ready yet.")
        else:
            methods.append("%d %s tomograms assigned to %d %s subtomograms." %
                           (self.inputTomos.get().getSize(), self.getObjectTag('inputTomos'),
                            self.inputSubtomos.get().getSize(), self.getObjectTag('inputSubtomos')))
        return methods
